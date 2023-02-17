from uuid import UUID

from pydantic import BaseModel
from pydantic.fields import Field

from pydantic_models.base import ResponseModel


class EventModel(ResponseModel):
    name: str

class PasswordModel(BaseModel):
    password: str = Field(min_length = 3, max_length = 35)

class EventModelWithId(EventModel):
    id: UUID

class EventModelWithPassword(EventModel, PasswordModel):
    ...

class EventModelFullDetail(EventModelWithId, PasswordModel):
    alive: bool
