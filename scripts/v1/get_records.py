from typing import List
from uuid import UUID

from db.singleton_handler import global_db_handler
from pydantic_models.record import RecordModel


def get_all_records(event_id: UUID) -> List[RecordModel]:
    "Returns all requested records from the db based on the *event_id*"
    db_handler = global_db_handler()
    result: List[RecordModel] = list()

    with db_handler.session() as session:
        ...

    return result