from typing import Any, Dict

from pydantic import BaseModel

from db.models.base import IDBModel


class ResponseModel(BaseModel):
    "This is the parent of every response model"
    @classmethod
    def convertFromOrm(cls, orm_obj: IDBModel):
        result: Dict[str, Any] = dict()

        for required_key in cls.__fields__:
            # NOTE: __dict__.get(...) does not work work fsr
            orm_value = getattr(orm_obj, required_key)

            if orm_value is None:
                raise ValueError(f"{required_key} is not present in the given orm object!")

            result[required_key] = orm_value

        return cls(**result)
