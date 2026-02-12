from schemas.user import UserID

class UserRepository:
    @classmethod
    async def get_user(cls, data: UserID) -> UserID:
        return UserID(
            id=data.id,
            username=data.username,
            role=data.role,
        )
