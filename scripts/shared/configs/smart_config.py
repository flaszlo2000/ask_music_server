from enum import Enum
from typing import Callable, Dict, Final, Generic, TypeVar

T_ENUM = TypeVar("T_ENUM", bound = Enum)

class SmartConfig(Generic[T_ENUM]):
    def __init__(self, config: Dict[T_ENUM, Callable[[], str]]) -> None:
        if len(config) == 0:
            raise AttributeError("The config must contain at least one element!")

        generic_enum_mapping = list(config.keys())[0].__class__.__members__
        config_keys = [key.name for key in config]

        key_mismatch = not all(map(lambda item: item in config_keys, generic_enum_mapping))
        if key_mismatch:
            raise AttributeError("The given config must map all the class' set generic enum's every element!")


        self._config: Final[Dict[T_ENUM, Callable[[], str]]] = config
        self._evaluated_config_elements: Dict[T_ENUM, str] = dict()

    def __getitem__(self, key: T_ENUM) -> str:
        """
        With this, late binding is achievable on config elements 
        which is needed when we need to access configuration from database which might be not present at the given moment of initialization.
        """
        # NOTE: every config element must be evaluated only once, and with this we cache it's value
        if key not in self._evaluated_config_elements:
            self._evaluated_config_elements[key] = self._config[key]()

        return self._evaluated_config_elements[key]
