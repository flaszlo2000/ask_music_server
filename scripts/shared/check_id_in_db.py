from http import HTTPStatus
from typing import Type, Union, overload
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from db.models.base import IDBModel
from db.models.events import DBEvents
from db.models.records import DBRecords


@overload
def check_id_in_db(session: Session, db_model: Type[DBEvents], _id: UUID) -> DBEvents:...
@overload
def check_id_in_db(session: Session, db_model: Type[DBRecords], _id: int) -> DBRecords:...
def check_id_in_db(
    session: Session,
    db_model: Type[IDBModel],
    _id: Union[UUID, int]
) -> IDBModel:
    inst_in_db = session.query(db_model).filter(db_model.id == _id).first()

    if inst_in_db is None:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            "Issue with the given id"
        )
    
    return inst_in_db