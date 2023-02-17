from fastapi import APIRouter

router = APIRouter()

@router.get("/events")
def get_ongoin_events():
    return "Hello"

@router.post("/event_login")
def try_to_login_to_event():
    return ""

@router.post("/music_request")
def send_music_request():
    ...