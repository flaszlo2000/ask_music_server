from typing import Dict, Final

USER_SCOPE: Final[Dict[str, str]] = {
    "user": "Normal user privilige, add records to current event",
}

ADMIN_SCOPE: Final[Dict[str, str]] = {
    **USER_SCOPE,
    "admin": "Admin priviliges",
}

MAINTAINER_2F_SCOPE: Final[Dict[str, str]] = {
    **ADMIN_SCOPE,
    "maintainer_2f": "Maintainer 2 factor auth page access",
}

MAINTAINER_SCOPE: Final[Dict[str, str]] = {
    **MAINTAINER_2F_SCOPE,
    "maintainer": "Handle admins"
}