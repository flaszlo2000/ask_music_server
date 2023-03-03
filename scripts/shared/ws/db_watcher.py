from dataclasses import dataclass, field
from threading import Event
from typing import List

from db.models.events import DBEvents
from db.models.records import DBRecords
from db.singleton_handler import global_db_handler
from pydantic_models.record import RecordModel
from scripts.shared.ws.base import IConnectionManager


@dataclass
class DBWatcher:
    ws_connection_manager: IConnectionManager
    stop_event: Event = field(default_factory = Event)
    poll_interval: float = field(default = 5)
    content: List[RecordModel] = field(default_factory = list)

    async def changeContent(self, new_content: List[RecordModel]) -> None:
        self.content = new_content
        await self.ws_connection_manager.broadcast(self.content)

    async def run(self) -> None:
        db_handler = global_db_handler()

        while not self.stop_event.wait(self.poll_interval):
            with db_handler.session() as session:
                #! FIXME: join
                active_event = session.query(DBEvents).filter(DBEvents.alive == True).first()               

                if active_event is None:
                    if len(self.content) > 0:
                        # if content has been saved already and the corresponding event gets disabled
                        # we empty the saved records and notify users 
                        await self.changeContent(list())

                    continue

                orm_records_for_active_event = session \
                    .query(DBRecords) \
                    .filter(DBRecords.f_event_id == active_event.id) \
                    .filter(DBRecords.done == False) \
                    .all()

                if len(orm_records_for_active_event) != len(self.content):
                    await self.changeContent([
                        RecordModel.convertFromOrm(orm_record) for orm_record in orm_records_for_active_event
                    ])

    def stop(self) -> None:
        self.stop_event.set()
