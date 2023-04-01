from dataclasses import dataclass, field
from datetime import datetime, timedelta
from random import choice
from typing import Final
from uuid import uuid4

CODE_EXPIRE_MINS: Final[int] = 2

@dataclass
class Code:
    code: str
    __expire_at: datetime = field(init = False)

    def __post_init__(self) -> None:
        self.__expire_at = datetime.now() + timedelta(minutes = CODE_EXPIRE_MINS)

    def isExpired(self) -> bool:
        return datetime.now() > self.__expire_at

    def __str__(self) -> str:
        return self.code

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Code) and not isinstance(__o, str): return False

        return self.code == str(__o)

    def __ne__(self, __o: object) -> bool:
        if not isinstance(__o, Code) and not isinstance(__o, str): return True
        
        return self.code != str(__o)

    def __hash__(self) -> int:
        return id(self) # hm

def get_secure_code() -> Code:
    uuid_segments = str(uuid4()).split('-')

    return Code(uuid_segments[0] + choice(uuid_segments[1:-1]))
