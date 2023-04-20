from enum import Enum

from fastapi.security import OAuth2PasswordBearer

from scripts import __version__


class Roles(str, Enum): # TODO: StrEnum in 3.11
    USER = "user"
    ADMIN = "admin"
    MAINTAINER_2F = "maintainer_2f"
    MAINTAINER = "maintainer"

oauth2_scheme = OAuth2PasswordBearer(f"{__version__}/token",
    scopes = {
        Roles.USER: "Normal user privilige, add records to current event",
        Roles.ADMIN: "Admin priviliges",
        Roles.MAINTAINER_2F: "Maintainer 2 factor auth page access",
        Roles.MAINTAINER: "Handle admins",
    }
)