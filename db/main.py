from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Generator

from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from db.check_tables import check_tables_on
from scripts.shared.dotenv_data import AllowedEnvKey, get_env_data


class BaseDbHandler(ABC):
    @contextmanager
    @abstractmethod
    def session(self) -> Generator[Session, None, None]:...

class DbHandler(BaseDbHandler):

    def __init__(self) -> None:
        super().__init__()
        self.engine: Engine = self.createEngine(
            get_env_data(AllowedEnvKey.DATABASE_URL)
        )
        check_tables_on(self.engine)

        self.sessionmaker = self.getSessionmaker()

    @staticmethod
    def createEngine(engine_uri: str) -> Engine:
        return create_engine(engine_uri)
    
    def getSessionmaker(
        self,
        *,
        autoflush: bool = False,
        autocommit: bool = False
    ) -> sessionmaker:
        return sessionmaker(bind = self.engine, autoflush = False, autocommit = False)

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        session = self.sessionmaker()

        yield session

        # session.expunge_all() # is this needed?
        session.close()