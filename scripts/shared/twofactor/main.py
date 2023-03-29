import requests
from sqlalchemy import desc

from db.models.app_config import DBAppConfig
from db.singleton_handler import global_db_handler
from scripts.shared.dotenv_data import AllowedEnvKey, get_env_data
from scripts.shared.twofactor.code_handler import Code


def get_2f_url() -> str:
    "Fetches the url from the db, if its not present then looks up .env and saves it from there"
    db_handler = global_db_handler()

    with db_handler.session() as session:
        last_config = session.query(DBAppConfig).order_by(desc(DBAppConfig.id)).first()

        if last_config is not None:
            return str(last_config.twofactor_webhooks_url)

        # no config yet
        result_url = get_env_data(AllowedEnvKey.WEBHOOKS_2F_URL)
        
        session.add(
            DBAppConfig(twofactor_webhooks_url = result_url)
        )

        session.commit()
    
    return result_url
            
def send_code_over_2f(code: Code) -> requests.Response:
    return requests.post(
        get_2f_url(),
        json = { "value1" : str(code) }
    )