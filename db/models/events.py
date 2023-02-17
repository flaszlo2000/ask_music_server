
from typing import Optional, Union
from uuid import UUID

from sqlalchemy import Boolean, Column, String, Uuid

from db.models.base import Base, IDBModel


class DBEvents(IDBModel, Base):
    __tablename__: str = "events"

    def __init__(
        self,
        id: UUID,
        name: str,
        password: str,
        note: Optional[str] = None,
        alive: bool = False
    ) -> None:
        super().__init__()
        self.id = id
        self.name = name
        self.password = password
        self.note = "" if note is None else note
        self.alive = alive

    # TODO: fix mypy error below
    id: Union[Column[UUID], UUID] = Column("id", Uuid, primary_key = True)
    name: Union[Column[str], str] = Column("name", String, nullable = False)
    password: Union[Column[str], str] = Column("password", String, nullable = False)
    note: Union[Column[str], str] = Column("note", String, default = "")
    alive: Union[Column[bool], bool] = Column("alive", Boolean, default = False)

    def __str__(self) -> str:
        return f"[{self.alive}] {self.id}:{self.name}** {self.password} ** - {self.note} -"