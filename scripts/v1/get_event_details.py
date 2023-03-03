from http import HTTPStatus
from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException

from db.models.events import DBEvents
from db.singleton_handler import global_db_handler
from pydantic_models.event import EventModelFullDetail, EventModelWithId
from scripts.shared.check_id_in_db import check_id_in_db


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
    "Returns all events from the db"
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
    db_handler = global_db_handler()

    with db_handler.session() as session:
        event_in_db = session \
            .query(DBEvents) \
            .filter(DBEvents.id == event_id) \
            .filter(DBEvents.password == password) \
            .first()

        if event_in_db is None:
            return False

    return True

def get_detailed_event(event_id: UUID) -> EventModelFullDetail:
    "Returns a specific event fully detailed based on *event_id*"
    result: EventModelFullDetail
    db_handler = global_db_handler()

    with db_handler.session() as session:
        event_in_db = check_id_in_db(session, DBEvents, event_id)

        result = EventModelFullDetail.convertFromOrm(event_in_db)

    return result

def get_detailed_current_event() -> EventModelFullDetail:
    "Returns the currently alive event's details without it's id"
    event_id: Optional[UUID] = None
    db_handler = global_db_handler()

    with db_handler.session() as session:
        orm_obj = session.query(DBEvents).filter(DBEvents.alive == True).first()

        if orm_obj is None:
            raise HTTPException(
                HTTPStatus.CONFLICT,
                "There is no running event!"
            )

        event_id = orm_obj.id

    return get_detailed_event(event_id)