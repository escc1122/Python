from typing import TypeVar, List

from sqlalchemy.orm import Session, Query

from SQLAlchemyTest.models.users_model import Users

T = TypeVar('T')


def create(db: Session, model: T) -> T:
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


def get_all(db: Session, model: T, skip: int = None, limit: int = None) -> List[T]:
    # 需要這樣取 不然會取到<class 'sqlalchemy.orm.decl_api.DeclarativeMeta'>
    model_class = model.__mapper__.class_
    query = db.query(model_class)

    query = _apply_filters_from_instance(query, model)


    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)

    models = query.all()
    return models


def get_users(db: Session, skip: int = None, limit: int = None):
    query = db.query(Users)

    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)

    return query.all()


def get_user(db: Session, user_id: int):
    return db.query(Users).filter(Users.id == user_id).first()


def update_user(db: Session, db_user: Users):
    db.commit()  # 提交更新
    db.refresh(db_user)  # 刷新資料，獲取最新資料
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(Users).filter(Users.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user


def _get_filters_from_instance(model:T) -> {}:
    model_class = model.__mapper__.class_
    filters = {}

    for column in model_class.__table__.columns:
        value = getattr(model, column.name, None)
        if value is not None:  # 只對非空值進行過濾
            filters[column] = value
    return filters


def _apply_filters_from_instance(query: Query, model:T) -> Query:
    filters = _get_filters_from_instance(model)
    # 添加過濾條件
    for column, value in filters.items():
        query = query.filter(column == value)

    return query
