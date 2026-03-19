from fastapi import HTTPException
from dependencies import CurrentUser
from enums.roles import Role

def admin_required(current_user: CurrentUser) -> None:
    if current_user.role is not Role.admin:
        raise HTTPException(status_code=403, detail="Forbidden")
