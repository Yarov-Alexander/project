from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.modules.users.schemas import UserCreate
from .models import User as UserModel

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def commit(self):
        await self.db.commit()

    async def refresh(self, user: UserModel):
        return await self.db.refresh(user)

    async def get_user_by_email(self, email: str) -> UserModel | None:
        result = await self.db.scalars(select(
            UserModel).where(
                UserModel.email == email,
                UserModel.is_active == True
            )
        )
        return result.first()

    async def create_user(self, email: str, password: str, role: str) -> UserModel:
        user_db = UserModel(
            email=email,
            hashed_password=password,
            role=role
        )
        self.db.add(user_db)
        return user_db