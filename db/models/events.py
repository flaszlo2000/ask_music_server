
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import Boolean, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import Base, IDBModel


class DBEvents(Base, IDBModel):
    __tablename__: str = "events"

    id: Mapped[UUID] = mapped_column("id", Uuid, primary_key = True)
    name: Mapped[str] = mapped_column("name", String, nullable = False)
    password: Mapped[str] = mapped_column("password", String, nullable = False)
    note: Mapped[str] = mapped_column("note", String, default = "")
    alive: Mapped[bool] = mapped_column("alive", Boolean, default = False)

    if TYPE_CHECKING:
        def __init__(
            self,
            id: UUID,
            name: str,
            password: str,
            note: Optional[str] = None,
            alive: bool = False
        ) -> None:...

    def __str__(self) -> str:
        return f"[{self.alive}] {self.id}:{self.name}** {self.password} ** - {self.note} -"