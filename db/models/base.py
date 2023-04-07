from typing import Any, Dict, Optional, Set

from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase, Mapped


class Base(DeclarativeBase):
    # NOTE: this must be the first class that a model inherits from.
    # If this is avoided then model creation won't work.
    # (l = Log(log = "test") but l's log field won't have any value!) 

    id: Mapped[Any]

    @classmethod
    def convertFromPydanticObject(
        cls,
        pydantic_object: BaseModel,
        exclude: Optional[Set[str]] = None,
        include: Optional[Dict[str, Any]] = None
    ):
        config_dict = pydantic_object.dict(
            exclude = set() if exclude is None else exclude
        )

        if include is not None:
            config_dict.update(include)

        return cls(**config_dict)