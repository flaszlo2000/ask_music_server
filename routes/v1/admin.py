from typing import Any, List

from fastapi import APIRouter, Body

from pydantic_models.event import EventModelWithPassword
from scripts.v1.add_new_event import new_event

admin_router = APIRouter(prefix = "/admin", tags = ["admin"])

@admin_router.post("/login")
def login():
    ...

@admin_router.post("/add_event")
def add_event(event_data: EventModelWithPassword = Body(...)):
    new_event(event_data)

@admin_router.post("/{event}/change_visibility")
def change_event_visibility():
    ...

@admin_router.post("/{event}/update")
def update_event_data():
    ...

@admin_router.get("/{event}/musics", response_model = List[Any]) # FIXME: type hint
def get_requested_musics():
    ...