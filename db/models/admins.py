from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import Base, IDBModel


class DBAdmins(IDBModel, Base):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column("id", Integer, primary_key = True, autoincrement = True)
    username: Mapped[str] = mapped_column("username", String, unique = True, nullable = False)
    password: Mapped[str] = mapped_column("password", String, nullable = False)
    webhooks_url: Mapped[str] = mapped_column("webhooks_url", String, nullable = True, unique = True)
    is_maintainer: Mapped[bool] = mapped_column("is_maintainer", Boolean, default = 0, nullable = False)

    if TYPE_CHECKING:
        def __init__(
            self,
            username: str, 
            password: str,
            webhooks_url: str,
            is_maintainer: bool = False,
            id: Optional[int] = None
        ) -> None:...

    def __str__(self) -> str:
        return f"{self.id}:{self.username} - {self.is_maintainer=} -"