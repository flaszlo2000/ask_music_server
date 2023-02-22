from uuid import UUID

from db.models.events import DBEvents
from db.singleton_handler import global_db_handler
from scripts.shared.check_id_in_db import check_id_in_db


def delete_event(event_id: UUID) -> None:
    db_handler = global_db_handler()

    with db_handler.session() as session:
        event_in_db = check_id_in_db(session, DBEvents, event_id)

        session.delete(event_in_db)
        session.commit()