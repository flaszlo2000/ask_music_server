from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Final, Optional, Union

CODE_EXPIRE_MINS: Final[int] = 1

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

class CodeHandler:
    def __init__(self, code: Optional[Code] = None, username: Optional[str] = None) -> None:
        self.__code = code
        self.username = username

    def checkIfCodeIsCorrect(self, given_code: Union[Code, str]) -> bool:
        if self.__code is None or self.__code.isExpired():
            return False

        return self.__code == given_code

    def add(self, code: Code, username: str) -> None:
        self.__code = code
        self.username = username