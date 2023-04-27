from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Security
from requests.exceptions import ConnectionError

from pydantic_models.admin import (AdminModel, DetailedAdminModel,
                                   FullAdminModel)
from routes.v1.dependencies import get_current_user_from_jwt, log_ip
from scripts.dependencies import full_maintainer_checked_token
from scripts.shared.security import Roles
from scripts.shared.security.twofactor import (get_secure_code,
                                               send_code_over_2f)
from scripts.static import code_handler
from scripts.v1.admin_handling import (add_admin_to_db, change_admin_in_db,
                                       delete_admin_from_db, get_all_admins)

base_maintainer_router = APIRouter(prefix = "/maintainer", tags = [Roles.MAINTAINER])
twofactor_router = APIRouter(prefix = "/2f_auth", tags = ["twofactor"]) # NOTE: be aware, each of this endpoints must depend on `maintainer_2f`

maintainer_router = APIRouter(dependencies = [
        Security(full_maintainer_checked_token, scopes = [Roles.MAINTAINER]),
        Depends(log_ip)
    ],
)

#region twofactor
@twofactor_router.post(
    "/send_code",
    responses = {
        int(key):value for key,value in {
            HTTPStatus.BAD_REQUEST: {"description": "No admin record in the db based on the given username that is a maintainer"},
            HTTPStatus.CONFLICT: {"description": "Missing webhooks url"},
            HTTPStatus.FAILED_DEPENDENCY: {"description": "Webhooks call returned with non 200 code"},
            HTTPStatus.UNAUTHORIZED: {"description": "Jwt error"},
            HTTPStatus.INTERNAL_SERVER_ERROR: {"description": "Cannot reach the given webhooks link"}
        }.items()
    }
)
async def send_code(current_user: str = Depends(get_current_user_from_jwt)):
    "Sends out twofactor token via webhooks" # TODO: google authenticator ?
    #! WARNING: at the first startup, env link will be used but then
    #! it is going to be added to the db and env won't be checked again
    secure_code = get_secure_code()
    code_handler.add(current_user, secure_code)

    try:
        response = send_code_over_2f(current_user, str(secure_code))

        if response.status_code != HTTPStatus.OK:
            raise HTTPException(
                HTTPStatus.FAILED_DEPENDENCY,
                "Unknown error during 2f notification sending"
            )
    except ConnectionError:
        raise HTTPException(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            "Connection outage"
        )
#endregion

@maintainer_router.post("/admins/add")
def add_admin(admin_credentials: DetailedAdminModel):
    add_admin_to_db(admin_credentials)

    # TODO: log
    print(f"*{admin_credentials.username}* has been added!")

@maintainer_router.get("/admins/get_all", response_model = List[AdminModel])
def get_admins():
    return get_all_admins()

@maintainer_router.put("/admins/update") # TODO: responses
def update_admin(updated_admin_model: FullAdminModel = Body(...)):
    #! DANGER: only the first maintainer will inherit the url from .env, but if all maintainers gets deleted
    #! for some reason, the .env url will be used again by generating automatically a new maintainer!
    #! This could lead to some interesting security risk.
    old_model: FullAdminModel = change_admin_in_db(updated_admin_model)

    # TODO: log
    print(f"*Admin with id: {updated_admin_model.id} has changed!*")
    # FIXME filter sensitive information
    # print("OLD:")
    # print(old_model)
    # print("NEW:")
    # print(updated_admin_model)

@maintainer_router.delete("/admins/delete")
def delete_admin(admin_id: int = Body(...)):
    delete_admin_from_db(admin_id)

    # TODO: log
    print(f"Admin [{admin_id}] has been deleted!")
