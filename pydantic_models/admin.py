from pydantic import BaseModel, Field, validator

from pydantic_models.base import ResponseModel
from scripts.shared.security import hash_pwd


class AdminConfigModel(BaseModel):
    username: str
    webhooks_url: str
    is_maintainer: bool = Field(default = False)

class PasswordConfigModel(BaseModel):
    password: str

    @validator("password")
    def encrypt(cls, v: str) -> str:
        # Make sure we don't handle plain password anywhere
        return hash_pwd(v)

# ResponseModel for classmethod to make it from 
class AdminModel(AdminConfigModel, ResponseModel):
    # OUT
    # everything except password
    id: int

class DetailedAdminModel(AdminConfigModel, PasswordConfigModel):
    # IN
    # everything except id
    ...

class FullAdminModel(AdminModel, PasswordConfigModel):
    # IN
    ...