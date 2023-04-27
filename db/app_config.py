from sqlalchemy import desc

from db.models import DBAppConfig
from db.singleton_handler import global_db_handler


def get_jwt_secret_key() -> str:
    # TODO: log this
    db_handler = global_db_handler()

    with db_handler.session() as session:
        app_config = session.query(DBAppConfig).order_by(desc(DBAppConfig.id)).limit(1).first()

        if app_config is None:
            raise RuntimeError("Insufficient appconfig")

        return app_config.jwt_key
