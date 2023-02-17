from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set

from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from typing_extensions import Protocol  # python3.7

Base = declarative_base()


class IDBModel(Protocol):
    __tablename__: str

    if TYPE_CHECKING:
        def __init__(self, *args: List[Any], **kwargs: Dict[str, Any]) -> None:
            ...

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