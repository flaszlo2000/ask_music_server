from sqlalchemy.ext.declarative import declarative_base
from typing_extensions import Protocol  # python3.7

Base = declarative_base()


class IDBModel(Protocol):
    __tablename__: str