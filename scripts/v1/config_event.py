from http import HTTPStatus
from uuid import UUID

from fastapi import HTTPException

from db.models.events import DBEvents
from db.singleton_handler import global_db_handler


def change_visibility_of(event_id: UUID, new_visibility: bool) -> None:
    "Changes visibility of an event"
    db_handler = global_db_handler()

    with db_handler.session() as session:
        event_in_db = session.query(DBEvents).filter(DBEvents.id == event_id).first()

        if event_in_db is None:
            raise HTTPException(
                HTTPStatus.BAD_REQUEST,
                "Issue with the given id"
            )
        
        if new_visibility:
            # NOTE: at a time, only one event can be run!
            running_event = session.query(DBEvents).filter(DBEvents.alive == True).first()

            if running_event is not None:
                raise HTTPException(
                    HTTPStatus.CONFLICT,
                    f"There is an event running already called *{running_event.name}*!"
                )

        event_in_db.alive = new_visibility
        session.commit()