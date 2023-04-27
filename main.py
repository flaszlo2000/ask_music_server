from typing import Iterable

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.access_ensure import check_db_for_maintainer
from db.singleton_handler import global_db_handler
from routes import ROUTERS
from scripts.shared.dotenv_data import (AllowedEnvKey, get_cors_conf,
                                        get_env_data)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = get_cors_conf(AllowedEnvKey.ALLOW_ORIGINS),
    allow_credentials = str(get_env_data(AllowedEnvKey.ALLOW_CREDENTIALS)).lower() == "true",
    allow_methods = get_cors_conf(AllowedEnvKey.ALLOW_METHODS),
    allow_headers = get_cors_conf(AllowedEnvKey.ALLOW_HEADERS)
)

def include_routers(routers: Iterable[APIRouter] = ROUTERS) -> None:
    "Includes the given routers into the global app"
    for router in routers:
        app.include_router(router)

@app.on_event("startup")
def startup() -> None:
    "Initializes the server startup requirements"
    db_handler = global_db_handler()
    check_db_for_maintainer(db_handler)

    include_routers()

    # TODO: generate and store user access key in db
    # it can be used in the JWT system to pass around an id
    # therefore it's *user_random_id* won't be needed
