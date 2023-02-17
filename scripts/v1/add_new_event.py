from db.models.events import DBEvents
from db.singleton_handler import global_db_handler
from db.unique_endpoint import get_unique_endpoint
from pydantic_models.event import EventModel


def new_event(event_data: EventModel) -> None:
    "Adds new event to the db"
    db_handler = global_db_handler()

    with db_handler.session() as session:
        orm_event_inst = DBEvents.convertFromPydanticObject(
            event_data,
            include = {
                "id": get_unique_endpoint()
            }
        )

        session.add(orm_event_inst)
        session.commit()