
from typing import Union
from uuid import UUID

from sqlalchemy import Boolean, Column, String, Uuid

from db.models.base import Base, IDBModel


class DBEvents(IDBModel, Base):
    __tablename__: str = "events"

    def __init__(self, id: UUID, name: str, password: str, alive: bool = False) -> None:
        super().__init__()
        self.id = id
        self.name = name
        self.password = password
        self.alive = alive

    # TODO: fix mypy error below
    id: Union[Column[Uuid], UUID] = Column("id", Uuid, primary_key = True)
    name: Union[Column[str], str] = Column("name", String, nullable = False)
    password: Union[Column[str], str] = Column("password", String, nullable = False)
    alive: Union[Column[Boolean], bool] = Column("alive", Boolean, default = False)

    def __str__(self) -> str:
        return f"{self.id}:{self.name}[{self.password}] - {self.alive} -"