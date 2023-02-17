from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Body, Path

from pydantic_models.event import EventModelWithId
from scripts.v1.add_new_record import new_record
from scripts.v1.get_events import ongoing_event

router = APIRouter()

@router.get("/event", response_model = Optional[EventModelWithId])
def get_ongoin_event():
    return ongoing_event()

@router.post("/event_login")
def try_to_login_to_event():
    return ""

@router.post("/{event_id}/record_request")
def send_record_request(
    event_id: UUID = Path(...),
    record_request: str = Body(...)
):
    new_record(event_id, record_request)