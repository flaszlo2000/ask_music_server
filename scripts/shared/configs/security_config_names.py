from enum import Enum, auto


class SecurityConfigNames(Enum):
    DEFAULT_EXP_MINS = auto()
    JWT_SECRET_KEY = auto()
    JWT_ALGORITHM = auto()