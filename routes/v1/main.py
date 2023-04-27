from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Body, Path, Security

from pydantic_models.event import EventModelWithId
from scripts.dependencies import user_checked_token
from scripts.shared.security import Roles
from scripts.v1.add_new_record import new_record
from scripts.v1.get_event_details import active_event

router = APIRouter()

@router.get("/event", response_model = Optional[EventModelWithId])
def get_ongoin_event():
    return active_event()

@router.post("/record_request/{event_id}")
def send_record_request(
    event_id: UUID = Path(...),
    record_request: str = Body(...),
    token: str = Security(user_checked_token, scopes = [Roles.USER])
):
    new_record(event_id, record_request)