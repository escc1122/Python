from typing import TypeVar, List
from sqlalchemy.orm import Session, Query


class DeleteException(Exception):
    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code

T = TypeVar('T')

def create(db: Session, model: T) -> T:
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


def select(db: Session, model: T, skip: int = None, limit: int = None) -> List[T]:
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


def update(db: Session, model: T):
    db.commit()
    db.refresh(model)
    return model


def delete(db: Session, model: T)->List[T]:
    # 確保傳入的是模型的實例，而不是類
    if isinstance(model, type):
        raise DeleteException("不允許不帶條件刪除，必須傳入實例")

    filters = _get_filters_from_instance(model)
    if len(filters)==0:
        raise DeleteException("不允許不帶條件刪除")

    delete_models = select(db,model)

    for d in delete_models:
        db.delete(d)

    db.commit()
    return delete_models

def _get_filters_from_instance(model: T) -> {}:
    model_class = model.__mapper__.class_
    filters = {}

    for column in model_class.__table__.columns:
        value = getattr(model, column.name, None)
        if value is not None:  # 只對非空值進行過濾
            filters[column] = value
    return filters


def _apply_filters_from_instance(query: Query, model: T, filters: {} = None) -> Query:
    if filters is None:
        filters = _get_filters_from_instance(model)
    # 添加過濾條件
    for column, value in filters.items():
        query = query.filter(column == value)

    return query
