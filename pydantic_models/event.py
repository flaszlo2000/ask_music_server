from uuid import UUID

from pydantic.fields import Field

from pydantic_models.base import ResponseModel


class EventModel(ResponseModel):
    name: str

class EventModelWithId(EventModel):
    uuid: UUID

class EventModelWithPassword(EventModel):
    password: str = Field(min_length = 3, max_length = 35)