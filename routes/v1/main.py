from uuid import UUID

from fastapi import APIRouter, Path

router = APIRouter()

@router.get("/events")
def get_ongoin_events():
    return ""

@router.post("/event_login")
def try_to_login_to_event():
    return ""

@router.post("/{event}/music_request")
def send_music_request(event: UUID = Path(...)):
    ...