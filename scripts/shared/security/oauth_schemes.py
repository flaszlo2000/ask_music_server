from fastapi.security import OAuth2PasswordBearer

from scripts import __version__
from scripts.shared.security.oauth_scopes import (ADMIN_SCOPE,
                                                  MAINTAINER_2F_SCOPE,
                                                  MAINTAINER_SCOPE, USER_SCOPE)

user_ouath2_scheme = OAuth2PasswordBearer(
    f"{__version__}/event_login",
    scopes = USER_SCOPE,
    scheme_name = "user_ouath2_scheme"
)

admin_oauth2_scheme = OAuth2PasswordBearer(
    f"{__version__}/admin/token",
    scopes = ADMIN_SCOPE,
    scheme_name = "admin_oauth2_scheme"
)

twofactor_maintainer_oauth2_scheme = OAuth2PasswordBearer(
    f"{__version__}/maintainer/token",
    scopes = MAINTAINER_2F_SCOPE,
    scheme_name = "twofactor_maintainer_oauth2_scheme"
)

full_maintainer_oauth2_scheme = OAuth2PasswordBearer(
    f"{__version__}/maintainer/2f_auth/login",
    scopes = MAINTAINER_SCOPE,
    scheme_name = "full_maintainer_oauth2_scheme"
)