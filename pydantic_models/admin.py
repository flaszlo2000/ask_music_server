from pydantic import BaseModel, Field

from pydantic_models.base import ResponseModel


class AdminConfigModel(BaseModel):
    username: str
    is_maintainer: bool = Field(default = False)

class PasswordConfigModel(BaseModel):
    password: str

class AdminModel(ResponseModel):
    id: int

# ResponseModel for classmethod to make it from 
class DetailedAdminConfigModel(AdminConfigModel, PasswordConfigModel, ResponseModel):... # input from admin addition

class FullAdminConfigModel(AdminModel, PasswordConfigModel):... # update admin