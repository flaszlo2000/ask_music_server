import asyncio
from signal import SIGINT, signal
from threading import Thread
from typing import Iterable

from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from db.main import DbHandler
from db.singleton_handler import global_db_handler
from routes import ROUTERS
from scripts.shared.dotenv_data import (AllowedEnvKey, get_cors_conf,
                                        get_env_data, get_env_file_path)
from scripts.shared.ws.connection_manager import WSConnectionManager

app = FastAPI()
load_dotenv(get_env_file_path())

app.add_middleware(
    CORSMiddleware,
    allow_origins = get_cors_conf(AllowedEnvKey.ALLOW_ORIGINS),
    allow_credentials = str(get_env_data(AllowedEnvKey.ALLOW_CREDENTIALS)).lower() == "true",
    allow_methods = get_cors_conf(AllowedEnvKey.ALLOW_METHODS),
    allow_headers = get_cors_conf(AllowedEnvKey.ALLOW_HEADERS)
)

ws_connection_manager = WSConnectionManager()
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
    global_db_handler(
        DbHandler(AllowedEnvKey.DATABASE_URL)
    )
    include_routers()
    init_db_polling()    

@app.on_event("shutdown")
def shutdown() -> None:
    ws_connection_manager.stop_db_poll()
    db_poll_thread.join()

@app.websocket("/ws/undone_records") # TODO: admin
async def ws_records(websocket: WebSocket):
    await ws_connection_manager.connect(websocket)

    try:
        data = await websocket.receive_text()
        print(data) # TODO remove this
    except WebSocketDisconnect:
        ws_connection_manager.disconnect(websocket)
