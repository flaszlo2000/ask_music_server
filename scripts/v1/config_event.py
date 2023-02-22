from http import HTTPStatus
from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from db.models.events import DBEvents
from db.singleton_handler import global_db_handler
from pydantic_models.event import EventModelFullDetail
from scripts.shared.check_id_in_db import check_id_in_db


def get_running_event_name(session: Session) -> Optional[str]:
    "Get the running event's name if there is one"
    running_event_name: Optional[str] = None

    running_event = session.query(DBEvents).filter(DBEvents.alive == True).first()
    if running_event is not None:
        running_event_name = str(running_event.name)

    return running_event_name

def check_if_there_is_no_runnning_event(session: Session) -> None:
    running_event_name = get_running_event_name(session)
    if running_event_name is not None:
        # NOTE: at the same time, only one event can be run!
        raise HTTPException(
            HTTPStatus.CONFLICT,
                f"There is an event running already called *{running_event_name}*!"
            )
    
def config_event(updated_event_model: EventModelFullDetail) -> None:
    "This makes every event updateable"
    db_handler = global_db_handler()

    with db_handler.session() as session:
        event_in_db = check_id_in_db(session, DBEvents, updated_event_model.id)

        if event_in_db.alive != updated_event_model.alive and updated_event_model.alive:
            check_if_there_is_no_runnning_event(session)

        session \
            .query(DBEvents) \
            .filter(DBEvents.id == updated_event_model.id) \
            .update(updated_event_model.dict())

        session.commit()

# FIXME: redundant function
def config_event_state(event_id: UUID, new_state: bool) -> None:
    "Function to make event state switch easier"
    db_handler = global_db_handler()

    with db_handler.session() as session:
        event_in_db = check_id_in_db(session, DBEvents, event_id)

        if not event_in_db.alive and new_state:
            check_if_there_is_no_runnning_event(session)

        event_in_db.alive = new_state
        session.commit()