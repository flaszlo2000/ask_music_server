from sqlalchemy import Boolean, Column, String, Uuid

from db.models.base import Base, IDBModel


class DBEvents(IDBModel, Base):
    __tablename__: str = "events"

    uuid = Column("id", Uuid, primary_key = True)
    name = Column("name", String, nullable = False)
    password = Column("password", String, nullable = False)
    alive = Column("alive", Boolean, default = False)