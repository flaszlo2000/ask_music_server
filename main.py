import asyncio
from signal import SIGINT, signal
from threading import Thread
from typing import Iterable

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.access_ensure import check_db_for_maintainer
from db.main import DbHandler
from db.singleton_handler import global_db_handler
from routes import ROUTERS
from scripts.shared.dotenv_data import (AllowedEnvKey, get_cors_conf,
                                        get_env_data)
from scripts.static import ws_connection_manager

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = get_cors_conf(AllowedEnvKey.ALLOW_ORIGINS),
    allow_credentials = str(get_env_data(AllowedEnvKey.ALLOW_CREDENTIALS)).lower() == "true",
    allow_methods = get_cors_conf(AllowedEnvKey.ALLOW_METHODS),
    allow_headers = get_cors_conf(AllowedEnvKey.ALLOW_HEADERS)
)

pararell_event_loop: asyncio.AbstractEventLoop

def run_db_watch():
    pararell_event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(pararell_event_loop)

    assert ws_connection_manager.db_watcher is not None

    pararell_event_loop.run_until_complete(ws_connection_manager.db_watcher.run())
    pararell_event_loop.close()

db_poll_thread = Thread(target = run_db_watch)

def include_routers(routers: Iterable[APIRouter] = ROUTERS) -> None:
    "Includes the given routers into the global app"
    for router in routers:
        app.include_router(router)

def init_db_polling() -> None:
    signal(SIGINT, lambda _, __: ws_connection_manager.stop_db_poll())
    db_poll_thread.start()

@app.on_event("startup")
def startup() -> None:
    "Initializes the server startup requirements"
    db_handler = global_db_handler(
        DbHandler(AllowedEnvKey.DATABASE_URL)
    )
    check_db_for_maintainer(db_handler)

    include_routers()
    init_db_polling()

    # TODO: generate and store user access key in db
    # it can be used in the JWT system to pass around an id
    # therefore it's *user_random_id* won't be needed

@app.on_event("shutdown")
def shutdown() -> None:
    ws_connection_manager.stop_db_poll()
    db_poll_thread.join()