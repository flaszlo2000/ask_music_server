from sqlalchemy import Column, Integer, String

from db.models.base import Base, IDBModel


class DBAdmins(IDBModel, Base):
    __tablename__ = "admins"

    id = Column("id", Integer, primary_key = True, autoincrement = True)
    username = Column("username", String, unique = True, nullable = False)
    password = Column("password", String, nullable = False)
