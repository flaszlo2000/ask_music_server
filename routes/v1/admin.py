from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Body, Path

from pydantic_models.event import EventModelFullDetail, EventModelWithPassword
from scripts.v1.add_new_event import new_event
from scripts.v1.config_event import change_visibility_of
from scripts.v1.get_events import get_all_event

admin_router = APIRouter(prefix = "/admin", tags = ["admin"])

@admin_router.post("/login")
def login():
    ...

@admin_router.post("/add_event")
def add_event(event_data: EventModelWithPassword = Body(...)):
    "Adds a new event to the db"
    new_event(event_data)

@admin_router.get("/events", response_model = List[EventModelFullDetail])
def get_events():
    "Returns all events in detail"
    return get_all_event()

@admin_router.post("/{event_id}/change_visibility")
def change_event_visibility(
    event_id: UUID = Path(...),
    new_visibility: bool = Body(...)
):
    "This endpoint is responsible to be able to start/stop an event"
    change_visibility_of(event_id, new_visibility)

@admin_router.post("/{event_id}/update")
def update_event_data(event_id: UUID):
    "Updates an event in the db based on the given *event_id*"
    ...

@admin_router.get("/{event_id}/musics", response_model = List[Any]) # FIXME: type hint
def get_requested_musics(event_id: UUID):
    "Returns all the requested music from the db"
    ...