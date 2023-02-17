from http import HTTPStatus

from fastapi import HTTPException

from db.models.records import DBRecords
from db.singleton_handler import global_db_handler


def change_record_state(record_id: int, *, new_state: bool) -> None:
    db_handler = global_db_handler()

    with db_handler.session() as session:
        orm_record = session.query(DBRecords).filter(DBRecords.id == record_id).first()

        if orm_record is None:
            raise HTTPException(
                HTTPStatus.BAD_REQUEST,
                "Issue with the id"
            )

        orm_record.done = new_state
        session.commit()