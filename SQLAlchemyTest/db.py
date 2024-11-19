from sqlalchemy import create_engine
from SQLAlchemyTest.config import mysql_config


def get_engine():
    # 替換以下信息以符合你的 MySQL 數據庫配置
    username = mysql_config['user']
    password = mysql_config['password']
    host = mysql_config['host']
    port = mysql_config['port']
    database = mysql_config['database']

    # 創建 MySQL 數據庫引擎
    engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}')

    # 測試連接
    try:
        # 嘗試連接到數據庫
        with engine.connect() as connection:
            print("成功連接到 MySQL 數據庫！")
    except Exception as e:
        print(f"連接 MySQL 數據庫失敗：{e}")

    return engine
