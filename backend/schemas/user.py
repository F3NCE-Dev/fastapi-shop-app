from pydantic import BaseModel, Field, StringConstraints
from typing import Annotated

UsernameStr = Annotated[str, StringConstraints(min_length=1, max_length=25, pattern=r"^[a-zA-Z0-9_-]+$")]

class UserAuth(BaseModel):
    username: UsernameStr = Field(examples=["username"])
    password: str = Field(min_length=5, max_length=25, examples=["password"])

class UserID(BaseModel):
    id: int
    username: str
    role: str
