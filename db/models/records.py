from typing import Optional, Union
from uuid import UUID

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import relationship

from db.models.base import Base, IDBModel


class DBRecords(IDBModel, Base):
    __tablename__: str = "records"

    def __init__(
        self,
        f_event_id: UUID,
        value: str,
        id: Optional[int] = None,
        done: bool = False
    ) -> None:
        super().__init__()

        if id is not None:
            self.id = id

        self.f_event_id = f_event_id
        self.value = value
        self.done = done

    id: Union[Column[int], int] = Column("id", Integer, primary_key = True)
    f_event_id: Union[Column[UUID], UUID] = Column("f_event_id", Uuid, ForeignKey("events.id"))
    value: Union[Column[str], str] = Column("value", String, nullable = False)
    done: Union[Column[bool], bool] = Column("done", Boolean, default = False)
    # TODO: possible duration

    event_id = relationship("DBEvents")

    def __str__(self) -> str:
        return f"[{self.f_event_id}] - {self.done} - {self.id}: {self.value} "