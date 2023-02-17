from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Path

from pydantic_models.event import EventModelWithId
from scripts.v1.get_ongoing_event import ongoing_event

router = APIRouter()

@router.get("/event", response_model = Optional[EventModelWithId])
def get_ongoin_event():
    return ongoing_event()

@router.post("/event_login")
def try_to_login_to_event():
    return ""

@router.post("/{event}/music_request")
def send_music_request(event: UUID = Path(...)):
    ...