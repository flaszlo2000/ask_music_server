from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base, IDBModel


class DBRecords(Base, IDBModel):
    __tablename__: str = "records"

    id: Mapped[int] = mapped_column("id", Integer, primary_key = True)
    f_event_id: Mapped[UUID] = mapped_column("f_event_id", Uuid, ForeignKey("events.id"))
    value: Mapped[str] = mapped_column("value", String, nullable = False)
    done: Mapped[str] = mapped_column("done", Boolean, default = False)
    # TODO: possible duration

    event_id = relationship("DBEvents")


    if TYPE_CHECKING:
        def __init__(
            self,
            f_event_id: UUID,
            value: str,
            id: Optional[int] = None,
            done: bool = False
        ) -> None:...

    def __str__(self) -> str:
        return f"[{self.f_event_id}] - {self.done=} - {self.id}: {self.value} "