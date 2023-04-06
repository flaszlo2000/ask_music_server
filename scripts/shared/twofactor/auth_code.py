from dataclasses import dataclass, field
from datetime import datetime, timedelta
from random import choice
from secrets import compare_digest
from typing import Final
from uuid import uuid4

CODE_EXPIRE_MINS: Final[int] = 2

@dataclass
class AuthCode:
    code: str
    __expire_at: datetime = field(init = False)

    def __post_init__(self) -> None:
        self.__expire_at = datetime.now() + timedelta(minutes = CODE_EXPIRE_MINS)

    def isExpired(self) -> bool:
        return datetime.now() > self.__expire_at

    def __str__(self) -> str:
        return self.code

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, AuthCode) and not isinstance(__o, str): return False

        input_pwd: str = str(__o)
        if not input_pwd.isascii():
            # compare_digest only accepts ascii chars
            return False

        return compare_digest(self.code, input_pwd)

    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)

    def __hash__(self) -> int:
        return id(self) # hm

def get_secure_code() -> AuthCode:
    uuid_segments = str(uuid4()).split('-')

    return AuthCode(uuid_segments[0] + choice(uuid_segments[1:-1]))
