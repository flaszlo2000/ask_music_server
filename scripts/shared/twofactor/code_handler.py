from typing import Dict, Optional, Union

from typing_extensions import overload

from scripts.shared.twofactor.code import Code


class CodeHandler:
    @overload
    def __init__(self, username: str, code: Code) -> None:...
    @overload
    def __init__(self, username: None = None, code: None = None) -> None:...
    def __init__(self, username: Optional[str] = None, code: Optional[Code] = None) -> None:
        self.__content: Dict[str, Code] = dict()

        if username is not None and code is not None:
            self.add(username, code)
        elif any([username, code]):
            raise AttributeError("Either both parameters are required or None")

    def checkIf2FCodeIsCorrect(self, username: str, given_code: Union[Code, str]) -> bool:
        saved_code = self.__content.get(username)

        if saved_code is None or saved_code.isExpired():
            return False

        return saved_code == str(given_code)

    def add(self, username: str, code: Code) -> None:
        self.__content[username] = code

    def forget(self, username: str) -> None:
        self.__content.pop(username)
