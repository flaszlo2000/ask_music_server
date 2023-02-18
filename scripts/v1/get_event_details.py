from http import HTTPStatus
from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException

from db.models.events import DBEvents
from db.singleton_handler import global_db_handler
from pydantic_models.event import EventModelFullDetail, EventModelWithId


def ongoing_event() -> Optional[EventModelWithId]:
    "Returns the currently active event"
    db_handler = global_db_handler()
    result: Optional[EventModelWithId] = None

    with db_handler.session() as session:
        current_event = session.query(DBEvents).filter(DBEvents.alive == True).first()

        if current_event is not None:
            result = EventModelWithId.convertFromOrm(current_event)
    
    return result

def get_all_event() -> List[EventModelFullDetail]:
    db_handler = global_db_handler()
    result: List[EventModelFullDetail] = list()

    with db_handler.session() as session:
        for orm_inst in session.query(DBEvents).all():
            result.append(
                EventModelFullDetail.convertFromOrm(orm_inst)
            )

    return result

def is_correct_password_for_event(event_id: UUID, password: str) -> bool:
    "Login for event"
    result = False
    db_handler = global_db_handler()

    with db_handler.session() as session:
        event_in_db = session \
            .query(DBEvents) \
            .filter(DBEvents.id == event_id) \
            .filter(DBEvents.password == password) \
            .first()

        if event_in_db is None:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Incorrect credentails!")

        result = True

    return result