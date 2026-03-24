from fastapi import HTTPException
from app.dependencies import CurrentUser
from app.enums.roles import Role

def admin_required(current_user: CurrentUser) -> None:
    if current_user.role is not Role.admin:
        raise HTTPException(status_code=403, detail="Forbidden")
