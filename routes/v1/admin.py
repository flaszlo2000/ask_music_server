from typing import List
from uuid import UUID

from fastapi import (APIRouter, Body, Path, Security, WebSocket,
                     WebSocketDisconnect)

from pydantic_models.event import EventModelFullDetail, EventModelWithPassword
from pydantic_models.record import RecordModel
from scripts.dependencies import admin_checked_token
from scripts.shared.security import Roles
from scripts.static import ws_connection_manager
from scripts.v1.add_new_event import new_event
from scripts.v1.config_event import config_event, config_event_state
from scripts.v1.config_record import change_record_state
from scripts.v1.delete_event import delete_event as crud_delete_event
from scripts.v1.get_event_details import (get_all_event,
                                          get_detailed_current_event,
                                          get_detailed_event)
from scripts.v1.get_records import get_all_records

base_admin_router = APIRouter(prefix = "/admin", tags = [Roles.ADMIN])
admin_router = APIRouter(dependencies = [
        # NOTE: if an admin gets deleted but it has valid admin jwt,
        # it still won't be able to perform any admin actions anymore because each endpoint is
        # protected with this.
        Security(admin_checked_token, scopes = [Roles.ADMIN])
    ]
)

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

@admin_router.post("/event_state/{event_id}")
def change_event_state(event_id: UUID, new_state: bool = Body(...)):
    "makes events state easily changeable"
    config_event_state(event_id, new_state)

@admin_router.get("/detailed_event/{event_id}", response_model = EventModelFullDetail)
def get_full_detailed_event(event_id: UUID = Path(...)):
    "Returns the admin level detailed version of an event"
    return get_detailed_event(event_id)

@admin_router.get("/detailed_current_event", response_model = EventModelFullDetail)
def get_full_detailed_current_event():
    return get_detailed_current_event()

@admin_router.delete("/delete_event/{event_id}")
def delete_event(event_id: UUID = Path(...)):
    crud_delete_event(event_id)

@admin_router.get("/records/{event_id}", response_model = List[RecordModel], deprecated = True)
def get_requested_records(event_id: UUID = Path(...)):
    """
    Returns all the requested records from the db

    .. deprecated:: 0.7
       Use WebSocket connection instead
    """
    return get_all_records(event_id)

@admin_router.post("/finish_record/{record_id}")
def finish_record(record_id: int = Path(...)):
    "Sets a record's 'done' parameter to True"
    change_record_state(record_id, new_state = True)

@admin_router.websocket("/ws/undone_records")
async def ws_records(websocket: WebSocket):
    await ws_connection_manager.connect(websocket)

    try:
        data = await websocket.receive_text()
        print(data) # TODO remove this
    except WebSocketDisconnect:
        ws_connection_manager.disconnect(websocket)