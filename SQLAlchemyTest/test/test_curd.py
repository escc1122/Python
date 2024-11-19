import pytest
from sqlalchemy.orm import sessionmaker

from SQLAlchemyTest.db import get_engine

from SQLAlchemyTest.models.users_model import Users
from SQLAlchemyTest.repositories.curd import create, get_all, _get_filters_from_instance


# 測試用的資料庫設定
@pytest.fixture
def db_session():
    engine = get_engine()
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_create_user(db_session):
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


def test_get_all(db_session):
    cond_model = Users()
    users = get_all(db_session, cond_model, 0, 1)
    assert len(users) == 1

    cond_model = Users(email="123456")
    users = get_all(db_session, cond_model)
    assert len(users) == 2

    users = get_all(db_session, cond_model,0,1)
    assert len(users) == 1


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
