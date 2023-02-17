from sqlalchemy import Column, Integer, String

from db.models.base import Base, IDBModel


class DBEvents(Base, IDBModel):
    __tablename__: str = "events"

    id = Column("id", Integer, primary_key = True)
    name = Column("name", String, nullable = False)
    password = Column("password", String, nullable = False)