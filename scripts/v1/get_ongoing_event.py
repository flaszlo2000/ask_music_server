from typing import Optional

from db.models.events import DBEvents
from db.singleton_handler import global_db_handler
from pydantic_models.event import EventModel


def ongoing_event() -> Optional[EventModel]:
    db_handler = global_db_handler()
    result: Optional[EventModel] = None

    with db_handler.session() as session:
        current_event = session.query(DBEvents).filter(DBEvents.alive == True).first()

        if current_event is not None:
            result = EventModel.convertFromOrm(current_event)
    
    return result