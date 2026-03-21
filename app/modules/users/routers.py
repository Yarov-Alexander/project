from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .exceptions import UserAlreadyExistsError, InvalidCredentialsError
from.schemas import User as UserSchema, UserCreate
from .services import UserService
from app.core.dependcies import get_user_service


router = APIRouter(prefix="/users",
                   tags=["users"]
)


@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, user_service: UserService = Depends(get_user_service())) -> UserSchema:
    try:
        user = await user_service.create_user(user)
        return user
    except UserAlreadyExistsError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="User already exists"
        )


@router.post("/token", status_code=status.HTTP_201_CREATED)
async def token(form_data: OAuth2PasswordRequestForm = Depends(), user_service: UserService = Depends(get_user_service())):
    try:
        token = await user_service.login(form_data.username, form_data.password)
        return token
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"}
        )

