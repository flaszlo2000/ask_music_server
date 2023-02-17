from typing import Iterable

from fastapi import APIRouter, FastAPI

from routes import ROUTERS

app = FastAPI()

@app.on_event("startup")
def include_routers(routers: Iterable[APIRouter] = ROUTERS) -> None:
    "Includes the given routers into the global app"
    for router in routers:
        app.include_router(router)