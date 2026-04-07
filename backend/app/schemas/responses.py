from pydantic import BaseModel, ConfigDict

class StatusResponse(BaseModel):
    success: bool
    detail: str

class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str

    model_config = ConfigDict(from_attributes=True)
