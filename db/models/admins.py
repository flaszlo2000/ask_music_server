from typing import Optional, Union

from sqlalchemy import Boolean, Column, Integer, String

from db.models.base import Base, IDBModel


class DBAdmins(IDBModel, Base):
    __tablename__ = "admins"

    id: Union[Column[int], int] = Column("id", Integer, primary_key = True, autoincrement = True)
    username: Union[Column[str], str] = Column("username", String, unique = True, nullable = False)
    password: Union[Column[str], str] = Column("password", String, nullable = False)
    webhooks_url: Union[Column[str], str] = Column("webhooks_url", String, nullable = True, unique = True)
    is_maintainer: Union[Column[bool], bool] = Column("is_maintainer", Boolean, default = 0, nullable = False)

    def __init__(
        self,
        username: str, 
        password: str,
        webhooks_url: str,
        is_maintainer: bool = False,
        id: Optional[int] = None
    ) -> None:
        super().__init__()
        self.username = username
        self.password = password
        self.is_maintainer = is_maintainer
        self.webhooks_url = webhooks_url

        if id is not None:
            self.id = id

    def __str__(self) -> str:
        return f"{self.id}:{self.username} - {self.is_maintainer=} -"