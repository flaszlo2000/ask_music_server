from typing import Iterable

from sqlalchemy import MetaData, Table
from sqlalchemy.orm import Session

from db.models.base import Base, IDBModel

# def clear_orm_dict() -> Dict[str, Any]:...


def fast_records(session: Session, table: Table, metadata: MetaData = Base.metadata) -> Iterable[IDBModel]:
    # fast but not memory efficient
    return (elem for elem in session.query(table).all())

def slow_records(session: Session, table: Table, metadata: MetaData = Base.metadata) -> Iterable[IDBModel]:
    # slow but memory efficient
    _offset = 0

    while True:
        orm_obj = session.query(table).offset(_offset).first()

        if orm_obj is not None:
            yield orm_obj
        else:
            break

        _offset += 1