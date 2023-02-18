from db.models.records import DBRecords
from db.singleton_handler import global_db_handler
from scripts.shared.check_id_in_db import check_id_in_db


def change_record_state(record_id: int, *, new_state: bool) -> None:
    db_handler = global_db_handler()

    with db_handler.session() as session:
        orm_record = check_id_in_db(session, DBRecords, record_id)

        orm_record.done = new_state
        session.commit()