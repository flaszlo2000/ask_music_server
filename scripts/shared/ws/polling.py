import asyncio
from signal import SIGINT, signal
from threading import Thread

from scripts.static import ws_connection_manager

pararell_event_loop: asyncio.AbstractEventLoop

def run_db_watch():
    pararell_event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(pararell_event_loop)

    assert ws_connection_manager.db_watcher is not None

    pararell_event_loop.run_until_complete(ws_connection_manager.db_watcher.run())
    pararell_event_loop.close()


db_poll_thread = Thread(target = run_db_watch)

def init_db_polling() -> None:
    signal(SIGINT, lambda _, __: ws_connection_manager.stop_db_poll())
    db_poll_thread.start()