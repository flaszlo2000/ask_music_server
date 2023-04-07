from http import HTTPStatus

from fastapi import Request, Security

from scripts.dependencies import twofactor_maintainer_checked_token
from scripts.shared.http_exc import get_http_exc_with_detail
from scripts.shared.security import get_payload_from_token


#region maintainer
async def get_current_user_from_jwt(token: str = Security(twofactor_maintainer_checked_token, scopes = ["maintainer_2f"])) -> str:
    jwt_payload = get_payload_from_token(token)
    username = jwt_payload.get("sub")

    if username is None:
        raise get_http_exc_with_detail(
            HTTPStatus.UNAUTHORIZED,
            "Incorrect data"
        )

    return username

async def log_ip(request: Request) -> None:
    ... # TODO
#endregion