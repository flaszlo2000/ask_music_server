from uuid import UUID

from pydantic import BaseModel
from pydantic.fields import Field

from pydantic_models.base import ResponseModel


class EventModel(ResponseModel):
    name: str

class AdminExtensionModel(BaseModel):
    password: str = Field(min_length = 3, max_length = 35)
    note: str = Field(default = "", max_length = 100)

class EventModelWithId(EventModel):
    id: UUID

class EventModelWithPassword(EventModel, AdminExtensionModel):
    ...

class EventModelFullDetail(EventModelWithId, AdminExtensionModel):
    alive: bool
