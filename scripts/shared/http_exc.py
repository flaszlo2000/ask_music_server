from http import HTTPStatus
from typing import Any, Dict, Final

from fastapi import HTTPException

CONIFGS: Final[Dict[HTTPStatus, Dict[str, Any]]] = {
    HTTPStatus.UNAUTHORIZED: {
        "status_code": HTTPStatus.UNAUTHORIZED,
        "headers": {"WWW-Authenticate": "Bearer"} 
    }
}

def get_http_exc_with_detail(_status_code: HTTPStatus, _detail: str) -> HTTPException:
    return HTTPException(
        **CONIFGS[_status_code],
        detail = _detail
    )