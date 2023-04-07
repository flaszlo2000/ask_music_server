from http import HTTPStatus
from typing import Final, TypeVar

from sqlalchemy.orm import Query

from db.models.admins import DBAdmins
from db.singleton_handler import global_db_handler
from scripts.shared.http_exc import get_http_exc_with_detail

TOKEN_CHECKER_ERROR_MSG: Final[str] = "Could not validate credentials"

T = TypeVar("T")
async def __get_data_from_db_by_query(query: Query[T], username: str) -> T:
    data_in_db = query.filter(DBAdmins.username == username).first()

    if data_in_db is None:
        raise get_http_exc_with_detail(HTTPStatus.UNAUTHORIZED, TOKEN_CHECKER_ERROR_MSG)

    return data_in_db

async def check_admin_exist(username: str) -> None:
    db_handler = global_db_handler()

    with db_handler.session() as session:
        await __get_data_from_db_by_query(session.query(DBAdmins), username)

async def check_maintainer_permission(username: str) -> None:
    db_handler = global_db_handler()

    with db_handler.session() as session:
        maintainer_permission = await __get_data_from_db_by_query(
            session.query(DBAdmins.is_maintainer),
            username
        )

        is_permitted = maintainer_permission[0]
        if not is_permitted:
            raise get_http_exc_with_detail(HTTPStatus.UNAUTHORIZED, TOKEN_CHECKER_ERROR_MSG)
