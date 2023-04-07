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
    def __init__(self, db_url: AllowedEnvKey) -> None:
        super().__init__()
        self.engine: Engine = self.createEngine(
            get_env_data(db_url)
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
    ) -> sessionmaker[Session]:
        return sessionmaker(bind = self.engine, autoflush = autoflush)

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        session = self.sessionmaker()

        yield session

        session.close()