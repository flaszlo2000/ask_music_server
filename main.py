from typing import Iterable

from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI

from routes import ROUTERS

app = FastAPI()

def include_routers(routers: Iterable[APIRouter] = ROUTERS) -> None:
    "Includes the given routers into the global app"
    for router in routers:
        app.include_router(router)

@app.on_event("startup")
def startup() -> None:
    "Initializes the server startup requirements"
    load_dotenv()
    include_routers()