from fastapi import HTTPException
from permissions.roles import Role

def admin_required(role: Role) -> None:
    if role is not Role.ADMIN:
        raise HTTPException(status_code=403, detail="Forbidden")
