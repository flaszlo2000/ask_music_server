from pydantic_models.base import ResponseModel


class RecordModel(ResponseModel):
    id: int
    value: str
    done: bool