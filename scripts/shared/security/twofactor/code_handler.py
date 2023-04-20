from typing import Dict, Optional, Union

from typing_extensions import overload

from scripts.shared.security.twofactor.auth_code import AuthCode


class CodeHandler:
    @overload
    def __init__(self, username: str, code: AuthCode) -> None:...
    @overload
    def __init__(self, username: None = None, code: None = None) -> None:...
    def __init__(self, username: Optional[str] = None, code: Optional[AuthCode] = None) -> None:
        self.__content: Dict[str, AuthCode] = dict()

        if username is not None and code is not None:
            self.add(username, code)
        elif any([username, code]):
            raise AttributeError("Either both parameters are required or None")

    def checkIf2FCodeIsCorrect(self, username: str, given_code: Union[AuthCode, str]) -> bool:
        saved_code: Optional[AuthCode] = self.__content.get(username, None)

        if saved_code is None:
            return False
    
        if saved_code.isExpired():
            # TODO: log?
            self.forget(username)

            return False

        return saved_code == str(given_code)

    #region FIXME: make threadsafe
    def add(self, username: str, code: AuthCode) -> None:
        self.__content[username] = code

    def forget(self, username: str) -> None:
        self.__content.pop(username)
    #endregion