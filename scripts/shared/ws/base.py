from typing import List, Optional, Protocol

from pydantic_models.record import RecordModel

# TODO: make these not RecordModel bounded

class IDBWatcher(Protocol):
    content: List[RecordModel]

    async def run(self) -> None:...
    def stop(self) -> None:...


class IConnectionManager(Protocol):
    db_watcher: Optional[IDBWatcher]

    async def broadcast(self, msg: List[RecordModel]) -> None:...
    def stop_db_poll(self) -> None:...
