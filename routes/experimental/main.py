from fastapi import APIRouter

router = APIRouter(prefix = "/experimental", tags = ["experimental"])

@router.get("/meaning_of_life")
def the_meaning_of_life():
    return {"The meaning of life": 42}