from typing import TypeVar, List, Any

from pydantic import BaseModel
from sqlalchemy import Column
from sqlalchemy.orm import Session, Query, DeclarativeMeta

from SQLAlchemyTest.models.users_model import Base


class DeleteException(Exception):
    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code


T = TypeVar('T', bound=DeclarativeMeta)


def create(db: Session, model: T) -> T:
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


def select(db: Session, model: T, skip: int = None, limit: int = None) -> List[T]:
    model_class = model.__mapper__.class_
    query = db.query(model_class)

    query = _apply_filters(query, model)

    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)

    models = query.all()
    return models


def select_from_pydantic(db: Session, model: T, pydantic_model: BaseModel, skip: int = None,
                         limit: int = None) -> List[T]:
    model_class = model.__mapper__.class_
    query = db.query(model_class)

    filters = _get_filters_from_pydantic(model_class, pydantic_model)

    query = _apply_filters(query, model, filters=filters)

    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)

    models = query.all()
    return models


def update(db: Session, model: T) -> T:
    db.commit()
    db.refresh(model)
    return model


def delete(db: Session, model: T) -> List[T]:
    # 確保傳入的是模型的實例，而不是類
    if isinstance(model, type):
        raise DeleteException("不允許不帶條件刪除，必須傳入實例")

    filters = _get_filters_from_instance(model)
    if len(filters) == 0:
        raise DeleteException("不允許不帶條件刪除")

    delete_models = select(db, model)

    for d in delete_models:
        db.delete(d)

    db.commit()
    return delete_models


def _get_filters_from_instance(model: T) -> dict[Column, Any]:
    model_class = model.__mapper__.class_
    filters = {}

    for column in model_class.__table__.columns:
        value = getattr(model, column.name, None)
        if value is not None:  # 只對非空值進行過濾
            filters[column] = value
    return filters


def _get_filters_from_pydantic(model: type[Base], pydantic_model: BaseModel) -> dict[Column, Any]:
    model_class = model.__mapper__.class_
    filters = {}

    for field, value in pydantic_model.model_dump(exclude_none=True).items():
        if hasattr(model_class, field):  # 確保 model_class 有該屬性
            column = getattr(model_class, field, None)
            if column is not None and value is not None:  # 確保 column 存在且值不為 None
                filters[column] = value
    return filters


def _apply_filters(query: Query, model: T, filters: dict[Column, Any] = None) -> Query:
    if filters is None:
        filters = _get_filters_from_instance(model)
    # 添加過濾條件
    for column, value in filters.items():
        query = query.filter(column == value)

    return query
