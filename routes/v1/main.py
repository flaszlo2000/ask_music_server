from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Body, Path, Security

from pydantic_models.event import EventModelWithId
from scripts.dependencies import checked_token
from scripts.v1.add_new_record import new_record
from scripts.v1.get_event_details import (is_correct_password_for_event,
                                          ongoing_event)

router = APIRouter()

@router.get("/event", response_model = Optional[EventModelWithId])
def get_ongoin_event():
    return ongoing_event()

@router.post("/event_login/{event_id}", response_model = bool)
def try_to_login_to_event(event_id: UUID = Path(...), event_password: str = Body()):
    return is_correct_password_for_event(event_id, event_password)

@router.post("/record_request/{event_id}")
def send_record_request(
    event_id: UUID = Path(...),
    record_request: str = Body(...),
    token: str = Security(checked_token, scopes = ["user"])
):
    new_record(event_id, record_request)