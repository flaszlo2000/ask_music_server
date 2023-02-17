from typing import List
from uuid import UUID

from fastapi import APIRouter, Body, Path

from pydantic_models.event import EventModelFullDetail, EventModelWithPassword
from pydantic_models.record import RecordModel
from scripts.v1.add_new_event import new_event
from scripts.v1.config_event import config_event
from scripts.v1.config_record import change_record_state
from scripts.v1.get_events import get_all_event
from scripts.v1.get_records import get_all_records

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

@admin_router.post("/event_update")
def update_event_data(updated_event_model: EventModelFullDetail = Body(...)):
    "Updates an event in the db based on the given updated event model"
    config_event(updated_event_model)

@admin_router.get("/{event_id}/records", response_model = List[RecordModel])
def get_requested_records(event_id: UUID = Path(...)):
    "Returns all the requested records from the db"
    return get_all_records(event_id)

@admin_router.post("/record/{record_id}")
def finish_record(record_id: int = Path(...)):
    "Sets a record's 'done' parameter to True"
    change_record_state(record_id, new_state = True)