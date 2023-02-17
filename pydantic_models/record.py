from pydantic_models.base import ResponseModel


class RecordModel(ResponseModel):
    value: str
    done: bool