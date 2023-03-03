from typing import List

from fastapi import APIRouter
from typing_extensions import Final  # python3.7

from routes.experimental.main import router as experimental_router
from routes.v1 import router as v1_router
from routes.v1.admin import admin_router
from routes.v1.admin import base_admin_router as v1_admin_router
from routes.v1.main import router as v1_main_router

v1_admin_router.include_router(admin_router)

ALL_ROUTERS: Final[List[APIRouter]] = [
    v1_admin_router,
    v1_main_router,
    experimental_router
]

for router in ALL_ROUTERS:
    v1_router.include_router(router)

ROUTERS: Final[List[APIRouter]] = [
    v1_router
]