from typing import Iterable

from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.access_ensure import db_setup_check
from db.main import DbHandler
from db.singleton_handler import global_db_handler
from routes import ROUTERS
from scripts.shared.dotenv_data import (AllowedEnvKey, get_cors_conf,
                                        get_env_data, get_env_file_path)
from scripts.shared.ws.polling import db_poll_thread, init_db_polling
from scripts.static import ws_connection_manager

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
    load_dotenv(get_env_file_path())
    include_routers()

    db_handler = global_db_handler(
        DbHandler(AllowedEnvKey.DATABASE_URL)
    )
    db_setup_check(db_handler)

    init_db_polling()

    # TODO: generate and store user access key in db
    # it can be used in the JWT system to pass around an id
    # therefore it's *user_random_id* won't be needed


@app.on_event("shutdown")
def shutdown() -> None:
    ws_connection_manager.stop_db_poll()
    db_poll_thread.join()
