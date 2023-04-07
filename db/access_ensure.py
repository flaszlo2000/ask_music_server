from typing import Final

from sqlalchemy.orm import Session

from db.main import BaseDbHandler
from db.models.admins import DBAdmins
from scripts.shared.dotenv_data import AllowedEnvKey, get_env_data
from scripts.shared.security import hash_pwd
from scripts.shared.twofactor import get_secure_code
from scripts.shared.twofactor.main import send_first_maintainer_pwd

BUILT_IN_MAINTAINER_USERNAME: Final[str] = "admin"

def add_maintainer(session: Session, maintainer_name: str) -> str:
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
        SECURE_PWD: Final[str] = add_maintainer(session, BUILT_IN_MAINTAINER_USERNAME)
        session.commit()
    
    print("[*] WARNING: Maintainer level user was not found, added one to the db")
    
    send_first_maintainer_pwd(BUILT_IN_MAINTAINER_USERNAME, SECURE_PWD)
    # TODO: make log about this