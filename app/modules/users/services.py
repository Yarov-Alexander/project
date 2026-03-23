from app.modules.users.exceptions import UserAlreadyExistsError, InvalidCredentialsError
from app.modules.users.models import User as UserModel
from app.modules.users.repositories import UserRepository
from app.modules.users.schemas import UserCreate
from app.core.config import settings
from app.auth.securety import hash_password, create_refresh_token
from app.auth.securety import verify_password, create_access_token
import jwt

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
        refresh_token = create_refresh_token(data={
            'sub': user.email,
            'role': user.role,
            'id': user.id}
        )
        return {"access_token": access_token, 'refresh_token': refresh_token, "token_type": "bearer"}



    async def get_user(self, email: str) -> UserModel:
        return await self.user_repo.get_user_by_email(email)


    async def update_access_token(self, token: str) -> dict:
        old_access_token = token

        try:
            payload = jwt.decode(old_access_token, settings.secret_key, algorithms=[settings.algorithm])
            email: str | None = payload.get("sub")
            token_type = payload.get("token_type")

            if email is None or token_type!= "refresh_token":
                raise InvalidCredentialsError()
        except jwt.ExpiredSignatureError:
            raise
        except jwt.PyJWTError:
            raise

        user = await self.user_repo.get_user_by_email(email)
        if user is None:
            raise InvalidCredentialsError()

        new_access_token = create_access_token(data={"sub": user.email, "role": user.role, "id": user.id})
        return {"access_token": new_access_token, "token_type": "bearer"}


    async def update_refresh_token(self, token: str) -> dict:
        old_refresh_token = token

        try:
            payload = jwt.decode(old_refresh_token, settings.secret_key, algorithms=[settings.algorithm])
            email: str | None = payload.get("sub")
            token_type = payload.get("token_type")

            if email is None or token_type!= "refresh":
                raise InvalidCredentialsError()
        except jwt.ExpiredSignatureError:
            raise
        except jwt.PyJWTError:
            raise

        user = await self.user_repo.get_user_by_email(email)
        if user is None:
            raise InvalidCredentialsError()

        new_refresh_token = create_refresh_token(data={"sub": user.email, "role": user.role, "id": user.id})
        return {"access_token": new_refresh_token, "token_type": "bearer"}