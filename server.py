import sys
from dataclasses import dataclass, field
from functools import lru_cache
from multiprocessing import cpu_count
from typing import Any, Dict, NoReturn, Optional

from gunicorn.app.base import BaseApplication
from gunicorn.arbiter import Arbiter
from starlette.applications import Starlette

from db.main import DbHandler
from db.singleton_handler import global_db_handler
from main import app
from scripts.shared.dotenv_data import AllowedEnvKey, get_env_data
from scripts.shared.ws.polling import db_poll_thread, init_db_polling
from scripts.static import ws_connection_manager


@lru_cache
def get_max_worker_count_based_on_cpu() -> int:
    return (cpu_count() * 2) + 1

@dataclass
class ServerConfig:
    host: str
    port: int
    workers: Optional[int] = field(default = None) 
    worker_class: Optional[str] = field(default = None)

    def __post_init__(self) -> None:
        if self.workers is None:
            self.workers = get_max_worker_count_based_on_cpu()

    @property
    def bind(self) -> str:
        return f"{self.host}:{self.port}"

def onStartup():
    global_db_handler(
        DbHandler(AllowedEnvKey.DATABASE_URL)
    )

    init_db_polling()

def onShutdown():
    ws_connection_manager.stop_db_poll()
    db_poll_thread.join()

#region gunicorn setup/overrides
class CustomArbiter(Arbiter):
    def halt(self, reason: Optional[Any] = None, exit_status: int = 0) -> NoReturn: # type: ignore # super().halt won't return
        onShutdown()
        super().halt(reason, exit_status)

class StandaloneApplication(BaseApplication):
    def __init__(self, app: Starlette, options: Optional[Dict[str, Any]] = None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

    def run(self) -> None:
        try:
            CustomArbiter(self).run()
        except RuntimeError as e:
            print("\nError: %s\n" % e, file=sys.stderr)
            sys.stderr.flush()
#endregion

def main() -> None:
    onStartup()

    server_config = ServerConfig(
        host = get_env_data(AllowedEnvKey.HOST),
        port = get_env_data(AllowedEnvKey.PORT),
        workers = get_env_data(AllowedEnvKey.SERVICE_WORKERS),
        worker_class = "uvicorn.workers.UvicornWorker"
    )

    StandaloneApplication(app, server_config.__dict__).run()

if __name__ == '__main__':
    main()
