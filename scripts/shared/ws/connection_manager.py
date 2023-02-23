from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from fastapi import WebSocket

from pydantic_models.record import RecordModel
from scripts.shared.ws.base import IConnectionManager, IDBWatcher
from scripts.shared.ws.db_watcher import DBWatcher


@dataclass
class WSConnectionManager(IConnectionManager):
    connections: List[WebSocket] = field(default_factory = list)
    db_watcher: Optional[IDBWatcher] = field(default = None)

    def __post_init__(self) -> None:
        if self.db_watcher is None:
            self.db_watcher = DBWatcher(self)

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.connections.append(websocket)
        
        await self.updateConnection(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        self.connections.remove(websocket)

    @staticmethod
    def get_format(data: List[RecordModel]) -> Dict[str, List[Dict[str, Any]]]:
        return { "data": [record.dict() for record in data] }

    async def updateConnection(self, websocket: WebSocket) -> None:
        assert self.db_watcher is not None

        await websocket.send_json(
            self.get_format(self.db_watcher.content)
        )

    async def broadcast(self, msg: List[RecordModel]) -> None:
        for connection in self.connections:
            await connection.send_json(
                self.get_format(msg)
            )

    def stop_db_poll(self) -> None:
        assert self.db_watcher is not None
        self.db_watcher.stop()