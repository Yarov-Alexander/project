from app.modules.users.exceptions import UserAlreadyExistsError, InvalidCredentialsError
from app.modules.users.models import User as UserModel
from app.modules.users.repositories import UserRepository
from app.modules.users.schemas import UserCreate

from app.auth.securety import hash_password
from app.auth.securety import verify_password, create_access_token


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo


    async def create_user(self, user: UserCreate) -> UserModel:
        existing = await self.user_repo.get_user_by_email(user.email)
        if existing:
            raise UserAlreadyExistsError()

        hashed_password = hash_password(user.password)
        result = await self.user_repo.create_user(
            user.email,
            hashed_password,
            role=user.role
        )

        await self.user_repo.commit()
        await self.user_repo.refresh(result)
        return result

    async def login(self, email: str, password: str) -> dict:
        user = await self.user_repo.get_user_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError()

        access_token  = create_access_token(data={
            "sub": user.email,
            "role": user.role,
            "id": user.id,
            }
        )
        return {"access_token": access_token, "token_type": "bearer"}

    async def get_user(self, email: str) -> UserModel:
        return await self.user_repo.get_user_by_email(email)
