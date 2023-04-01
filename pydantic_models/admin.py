from pydantic import BaseModel, Field

from pydantic_models.base import ResponseModel


class AdminConfigModel(BaseModel):
    username: str
    webhooks_url: str
    is_maintainer: bool = Field(default = False)

class PasswordConfigModel(BaseModel):
    password: str

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