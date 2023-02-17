from typing import Final, List

from fastapi import APIRouter

from routes.v1 import router as v1_router
from routes.v1.admin import admin_router as v1_admin_router
from routes.v1.main import router as v1_main_router

ALL_ROUTERS: Final[List[APIRouter]] = [
    v1_admin_router,
    v1_main_router
]

for router in ALL_ROUTERS:
    v1_router.include_router(router)

ROUTERS: Final[List[APIRouter]] = [
    v1_router
]