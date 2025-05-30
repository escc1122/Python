import pytest
from pydantic import BaseModel
from requests import session
from sqlalchemy import create_engine

from SQLAlchemyTest import db
from SQLAlchemyTest.models.users_model import Users, Base
from SQLAlchemyTest.repositories.curd import create, select, _get_filters_from_instance, update, delete, \
    DeleteException, _get_filters_from_pydantic, select_from_pydantic


# 用來獲取 SQLite 3 引擎
def get_engine():
    return create_engine("sqlite:///:memory:", echo=True)  # 使用內存中的 SQLite 資料庫


@pytest.fixture(autouse=True)
def before_setup(mocker):
    mocker.patch('SQLAlchemyTest.db.create_mysql_engine', return_value=get_engine())  # mock MySQL 引擎為 SQLite 引擎
    engine = db.get_engine()
    # 創建所有表格
    Base.metadata.create_all(bind=engine)


@pytest.fixture
def get_mock_session():
    return db.get_session


def test_create(get_mock_session):
    with get_mock_session() as db_session:
        # Arrange
        user = Users(name="Test User", email="test@example.com")

        # Act
        created_user = create(db_session, user)

        # Assert
        assert created_user.id is not None
        assert created_user.name == "Test User"
        assert created_user.email == "test@example.com"

        # 驗證資料是否存入資料庫
        db_user = db_session.query(Users).filter_by(id=created_user.id).first()
        assert db_user is not None
        assert db_user.name == "Test User"
        assert db_user.email == "test@example.com"

        # 刪除測試數據
        db_session.query(Users).filter(Users.email == "test@example.com").delete()
        db_session.commit()


def test_select(get_mock_session):
    with get_mock_session() as db_session:
        # 插入測試數據
        user1 = Users(name="Alice", email="alice@example.com")
        user2 = Users(name="Bob", email="bob@example.com")
        user3 = Users(name="test", email="alice@example.com")
        db_session.add(user1)
        db_session.add(user2)
        db_session.add(user3)
        db_session.commit()

        cond_model = Users()
        users = select(db_session, cond_model, 0, 1)
        assert len(users) == 1

        cond_model = Users(email="alice@example.com")
        users = select(db_session, cond_model)
        assert len(users) == 2

        users = select(db_session, cond_model, 0, 1)
        assert len(users) == 1

        users = select(db_session, Users())
        assert len(users) == 3

        # 刪除測試數據
        db_session.query(Users).filter(Users.email == "alice@example.com").delete()
        db_session.query(Users).filter(Users.email == "bob@example.com").delete()
        db_session.commit()


def test_update(get_mock_session):
    with get_mock_session() as db_session:
        user = Users(name="update", email="update@example.com")

        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)  # 確保將變更刷新到內存

        # 改變 user 的名稱並更新
        user.name = "Updated update"

        # 使用 update 函數進行更新
        updated_user = update(db_session, user)

        # 驗證更新是否成功
        db_session.refresh(updated_user)  # 確保從數據庫加載最新的數據
        assert updated_user.name == "Updated update"  # 驗證名稱是否更新
        assert updated_user.email == "update@example.com"  # 驗證其他屬性沒有變化

        # 刪除測試數據
        db_session.delete(updated_user)  # 刪除更新過的 user
        db_session.commit()  # 提交刪除操作


def test_delete(get_mock_session):
    with get_mock_session() as db_session:
        # 插入測試數據
        user1 = Users(name="delete", email="delete@example.com")
        user2 = Users(name="delete2", email="delete2@example.com")
        db_session.add(user1)
        db_session.add(user2)
        db_session.commit()

        # 測試有條件的刪除
        delete_user = Users(name="delete")  # 這個條件應該匹配 user1
        deleted_users = delete(db_session, delete_user)

        # 驗證刪除結果
        assert len(deleted_users) == 1  # 確保刪除了一個用戶
        assert deleted_users[0].name == "delete"  # 確保刪除的用戶是 Alice

        # 確認數據庫中 Alice 用戶已被刪除
        user_in_db = db_session.query(Users).filter(Users.name == "delete").first()
        assert user_in_db is None  # 確保用戶不再存在

        user_in_db = db_session.query(Users).filter(Users.name == "delete2").first()
        assert user_in_db is not None  # 確保用戶存在

        # 刪除測試數據
        db_session.query(Users).filter(Users.email == "delete2@example.com").delete()
        db_session.commit()


def test_delete_exception(get_mock_session):
    with get_mock_session() as db_session:
        # 測試不帶條件的刪除會拋出異常
        with pytest.raises(DeleteException):
            delete(db_session, Users())  # 不帶條件的刪除應該拋出 DeleteException

        # 測試不帶條件的刪除會拋出異常
        with pytest.raises(DeleteException):
            delete(db_session, Users)  # 不帶條件的刪除應該拋出 DeleteException


def test_get_filters_from_instance():
    users = Users(id=5, name="Test User", email="test@example.com")
    filters = _get_filters_from_instance(users)
    # 檢查結果
    expected_filters = {
        Users.__table__.c.id: 5,
        Users.__table__.c.name: "Test User",
        Users.__table__.c.email: "test@example.com",
    }

    assert filters == expected_filters, f"測試失敗！結果: {filters}, 預期: {expected_filters}"


def test_get_filters_from_instance2():
    users = Users(id=5, email="test@example.com")
    filters = _get_filters_from_instance(users)
    # 檢查結果
    expected_filters = {
        Users.__table__.c.id: 5,
        Users.__table__.c.email: "test@example.com",
    }

    assert filters == expected_filters, f"測試失敗！結果: {filters}, 預期: {expected_filters}"


# 定義 Pydantic 模型
class UserPydantic(BaseModel):
    name: str = None
    email: str = None

    class Config:
        orm_mode = True


def test_get_filters_from_pydantic():
    # 創建 Pydantic 模型實例
    pydantic_data = UserPydantic(name="Alice", email="alice@example.com")

    # 呼叫 _get_filters_from_pydantic 函數來獲得過濾條件
    filters = _get_filters_from_pydantic(Users, pydantic_data)

    # 測試過濾條件的結果是否符合預期
    assert len(filters) == 2  # 應該有 2 個過濾條件: name 和 email
    assert filters[Users.name] == "Alice"
    assert filters[Users.email] == "alice@example.com"


def test_select_from_pydantic(get_mock_session):
    with get_mock_session() as db_session:
        # 插入測試數據
        user1 = Users(name="Alice", email="alice@example.com")
        user2 = Users(name="Alice", email="bob@example.com")
        user3 = Users(name="test", email="alice@example.com")
        db_session.add(user1)
        db_session.add(user2)
        db_session.add(user3)
        db_session.commit()

    pydantic_data = UserPydantic(name="Alice", email="alice@example.com")

    users = select_from_pydantic(db_session, Users(), pydantic_data)

    assert len(users) == 1

    pydantic_data = UserPydantic(name="Alice")

    users = select_from_pydantic(db_session, Users(), pydantic_data)

    assert len(users) == 2
