from pydantic import BaseModel


class ResponseModel(BaseModel):
    "This is the parent of every response model"
    ...