from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import Base


class DBAppConfig(Base):
    __tablename__ = "app_config"

    id: Mapped[int] = mapped_column("id", Integer, primary_key = True, autoincrement = True)
    jwt_key: Mapped[str] = mapped_column("jwt_key", unique = True, nullable = False)
    session_key: Mapped[str] = mapped_column("session_key", String, nullable = False)

    if TYPE_CHECKING:
        def __init__(self, jwt_key: str, session_key: str):...

    def __str__(self) -> str:
        return f"[{self.id}] {self.jwt_key} - {self.session_key}"