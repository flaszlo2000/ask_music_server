from typing import Final

from sqlalchemy.orm import Session

from db.main import BaseDbHandler
from db.models.admins import DBAdmins
from db.models.app_config import DBAppConfig
from scripts.shared.dotenv_data import AllowedEnvKey, get_env_data
from scripts.shared.security import hash_pwd
from scripts.shared.security.twofactor import get_secure_code
from scripts.shared.security.twofactor.auth_code import get_long_secure_str
from scripts.shared.security.twofactor.main import send_first_maintainer_pwd

BUILT_IN_MAINTAINER_USERNAME: Final[str] = "admin"

def __add_maintainer(session: Session, maintainer_name: str) -> str:
    env_webhooks_url = get_env_data(AllowedEnvKey.INITIAL_WEBHOOKS_2F_URL)
    SECURE_PWD: Final[str] = "admin" #! FIXME str(get_secure_code())

    maintainer = DBAdmins(
        username = maintainer_name,
        password = hash_pwd(SECURE_PWD),
        webhooks_url = env_webhooks_url,
        is_maintainer = True
    )

    session.add(maintainer)
    return SECURE_PWD

def check_db_for_maintainer(db_handler: BaseDbHandler) -> None:
    "Check if there is at least one maintainer in db"
    with db_handler.session() as session:
        maintainer_count = session.query(DBAdmins).filter(DBAdmins.is_maintainer == True).count()

        if maintainer_count > 0: return

        # no config yet
        SECURE_PWD: Final[str] = __add_maintainer(session, BUILT_IN_MAINTAINER_USERNAME)
        session.commit()
    
    print("[*] WARNING: Maintainer level user was not found, added one to the db")
    
    send_first_maintainer_pwd(BUILT_IN_MAINTAINER_USERNAME, SECURE_PWD)
    # TODO: make log about this

def __add_random_secure_config(session: Session):
    session.add(
        DBAppConfig(
            jwt_key = get_long_secure_str(),
            session_key = get_long_secure_str() 
        )
    )

def check_db_for_config(db_handler: BaseDbHandler) -> None:
    with db_handler.session() as session:
        if session.query(DBAppConfig).first() is not None: return

        __add_random_secure_config(session)
        session.commit()

    print("[*] WARNING: Appconfig was not found in the db, added one")
    # TODO: log

def db_setup_check(db_handler: BaseDbHandler) -> None:
    check_db_for_maintainer(db_handler)
    check_db_for_config(db_handler)
