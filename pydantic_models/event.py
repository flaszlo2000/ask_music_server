from uuid import UUID

from pydantic_models.base import ResponseModel


class EventModel(ResponseModel):
    name: str
    uuid: UUID