from http import HTTPStatus

import requests
from fastapi import HTTPException

from db.models.admins import DBAdmins
from db.singleton_handler import global_db_handler


def get_webhooks_url(username: str) -> str:
    "Fetches the url from the db, if its not present then looks up .env and saves it from there"
    db_handler = global_db_handler()

    with db_handler.session() as session:
        admin_webhook_url_result = session \
            .query(DBAdmins.webhooks_url) \
            .filter(DBAdmins.is_maintainer == True) \
            .filter(DBAdmins.username == username) \
            .first() 

        if admin_webhook_url_result is None:
            # there is no record with the given name that is maintainer
            raise HTTPException(
                HTTPStatus.BAD_REQUEST,
                "Incorrect credentials"
            )

        admin_webhook_url = admin_webhook_url_result[0]
        if admin_webhook_url is None:
            # no webhooks url yet
            raise HTTPException(
                HTTPStatus.CONFLICT,
                "Missing twofactor credential, contact owner"
            )

        return str(admin_webhook_url)

def send_code_over_2f(username: str, code: str) -> requests.Response:
    return requests.post(
        get_webhooks_url(username),
        json = { "value1" : code }
    )

def send_first_maintainer_pwd(username: str, pwd: str) -> requests.Response:
    return send_code_over_2f(
        username,
        f"Maintainer added with: {pwd}. Please change this as fast as possible!"
    )