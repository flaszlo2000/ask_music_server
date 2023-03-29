from sqlalchemy import Column, Integer, String

from db.models.base import Base, IDBModel


class DBAppConfig(IDBModel, Base):
    __tablename__ = "app_config"

    id = Column("id", Integer, primary_key = True, autoincrement = True)
    twofactor_webhooks_url = Column("twofactor_webhooks_url", String)

    def __init__(self, twofactor_webhooks_url: str) -> None:
        super().__init__()
        self.twofactor_webhooks_url = twofactor_webhooks_url