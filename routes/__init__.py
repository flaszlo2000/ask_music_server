from typing import List

from fastapi import APIRouter
from typing_extensions import Final  # python3.7

from routes.experimental.main import router as experimental_router
from routes.v1 import router as v1_router
from routes.v1.admin import admin_router
from routes.v1.admin import base_admin_router as v1_admin_router
from routes.v1.main import router as v1_main_router
from routes.v1.maintainer import base_maintainer_router as v1_maintainer_router
from routes.v1.maintainer import maintainer_router, twofactor_router

v1_admin_router.include_router(admin_router)

v1_maintainer_router.include_router(twofactor_router)
v1_maintainer_router.include_router(maintainer_router)

ALL_ROUTERS: Final[List[APIRouter]] = [
    #! DONT FORGET TO CHANGE VERSION IN scripts/__init__.py, dependencies.py depends on it!
    v1_admin_router,
    v1_main_router,
    v1_maintainer_router,
    experimental_router
]

for router in ALL_ROUTERS:
    v1_router.include_router(router)

ROUTERS: Final[List[APIRouter]] = [
    v1_router
]