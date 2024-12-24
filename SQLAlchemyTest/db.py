import threading
from contextlib import contextmanager

from retry import retry
from sqlalchemy.exc import OperationalError
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from SQLAlchemyTest.config import mysql_config


def get_mysql_config() -> dict:
    """
    從配置文件中獲取 MySQL 配置。

    Args:
        None

    Returns:
        dict: 包含 MySQL 配置參數的字典。
            包括 user、password、host、port 和 database 名稱。
    """
    return {
        "user": mysql_config.get('user', 'root'),
        "password": mysql_config.get('password', ''),
        "host": mysql_config.get('host', 'localhost'),
        "port": mysql_config.get('port', 3306),
        "database": mysql_config.get('database', ''),
    }


def create_mysql_engine() -> Engine:
    """
    使用配置參數創建並返回一個 SQLAlchemy MySQL 引擎。

    Args:
        None

    Returns:
        Engine: 與 MySQL 資料庫建立連接的 SQLAlchemy 引擎實例。

    Raises:
        RuntimeError: 如果引擎創建過程中發生異常，則會拋出此異常。
    """
    config = get_mysql_config()
    engine_url = f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"

    try:
        inner_engine = create_engine(
            engine_url,
            pool_size=10,  # 連接池大小
            max_overflow=20,  # 最大額外連接數
            pool_timeout=30,  # 連接超時時間（秒）
            pool_recycle=1800,  # 連接回收時間（秒）
            echo=False,  # 設為 True 可啟用 SQL 查詢日誌（用於調試）
        )
        print("MySQL 引擎已成功創建！")
        return inner_engine
    except Exception as e:
        raise RuntimeError(f"無法創建 MySQL 引擎：{e}") from e

class MySQLSingletonEngine:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = create_mysql_engine()  # 假設 create_mysql_engine 是你創建引擎的函數
        return cls._instance


def get_engine():
    # 確保在需要時使用單例引擎
    return MySQLSingletonEngine()


def get_session_factory() -> sessionmaker:
    """
    返回一個與 MySQL 引擎綁定的 session 工廠。

    Args:
        None

    Returns:
        sessionmaker: 可以用來創建新 session 的 session 工廠。
    """
    return sessionmaker(bind=get_engine())

@contextmanager
@retry(OperationalError, tries=3, delay=5)
def get_session() -> Session:
    """
    上下文管理器，用於自動管理 SQLAlchemy Session 的創建與釋放。
    使用 retry 裝飾器來自動重試資料庫操作錯誤（例如連接問題）。

    Args:
        None

    Returns:
        Session: 用於與資料庫互動的 SQLAlchemy 活躍 session。

    Raises:
        OperationalError: 當資料庫連線中斷時，會重試 3 次。
    """
    session_factory = get_session_factory()
    session = session_factory()
    try:
        yield session  # 返回 session 以供 with 區塊使用
    except OperationalError as e:
        print(f"資料庫連線中斷，重試中... {e}")
        raise  # 重新拋出異常以便 retry 處理
    finally:
        # 關閉 session
        if session:
            session.close()
            print("Session 已關閉")

@retry(OperationalError, tries=3, delay=5)
def get_connection():
    """
    上下文管理器，用於自動管理 SQLAlchemy Connection 的創建與釋放。
    使用 retry 裝飾器來自動重試資料庫連接錯誤（例如連接中斷）。

    Args:
        None

    Returns:
        Connection: 用於與資料庫互動的 SQLAlchemy 連接。

    Raises:
        OperationalError: 當資料庫連線中斷時，會重試 3 次。
    """
    connection = get_engine().connect()
    try:
        yield connection  # 返回 connection 以供 with 區塊使用
    except OperationalError as e:
        print(f"資料庫連線中斷，重試中... {e}")
        raise  # 重新拋出異常以便 retry 處理
    finally:
        # 關閉 connection
        if connection:
            connection.close()
            print("資料庫連接已關閉")

