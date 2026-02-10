from pydantic import BaseModel

class StatusRespones(BaseModel):
    success: bool
    detail: str
