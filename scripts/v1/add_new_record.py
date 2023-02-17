from http import HTTPStatus
from uuid import UUID

from fastapi import HTTPException

from db.models.events import DBEvents
from db.models.records import DBRecords
from db.singleton_handler import global_db_handler


def new_record(event_id: UUID, record_value: str, *, only_ongoing: bool = True) -> None:
    "Adds a new record to the db that is in relationship with an event"
    db_handler = global_db_handler()

    with db_handler.session() as session:
        query_for_event_in_db = session.query(DBEvents).filter(DBEvents.id == event_id)

        if only_ongoing:
            # NOTE: only admin is able to add record request to an event that is not ongoing
            query_for_event_in_db = query_for_event_in_db.filter(DBEvents.alive == True)    

        event_in_db = query_for_event_in_db.first()

        if event_in_db is None:
            raise HTTPException(HTTPStatus.BAD_REQUEST)

        session.add(DBRecords(event_id, record_value))
        session.commit()