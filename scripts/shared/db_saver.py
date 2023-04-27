from typing import Iterable

from sqlalchemy import MetaData, Table
from sqlalchemy.orm import Session

from db.models.base import Base

# def clear_orm_dict() -> Dict[str, Any]:...


def fast_records(session: Session, table: Table, metadata: MetaData = Base.metadata) -> Iterable[Base]:
    # fast but not memory efficient
    return (elem for elem in session.query(table).all())

def slow_records(session: Session, table: Table, metadata: MetaData = Base.metadata) -> Iterable[Base]:
    # slow but memory efficient
    _offset = 0

    while True:
        orm_obj = session.query(table).offset(_offset).first()

        if orm_obj is not None:
            yield orm_obj
        else:
            break

        _offset += 1