from pydantic import BaseModel, StringConstraints, ConfigDict
from typing import Annotated
from enums.roles import Role

UsernameStr = Annotated[str, StringConstraints(min_length=1, max_length=25, pattern=r"^[a-zA-Z0-9_-]+$")]
PasswordStr = Annotated[str, StringConstraints(min_length=5, max_length=25)]

class UserAuth(BaseModel):
    username: UsernameStr
    password: PasswordStr

class UserID(BaseModel):
    id: int
    username: str
    role: Role

    model_config = ConfigDict(from_attributes=True)

class User(BaseModel):
    id: int
    username: str
    role: Role
    profile_picture_url: str

    model_config = ConfigDict(from_attributes=True)

class NewUsername(BaseModel):
    new_name: str = UsernameStr

class NewPassword(BaseModel):
    password: PasswordStr
