from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .exceptions import UserAlreadyExistsError, InvalidCredentialsError
from .schemas import User as UserSchema, UserCreate, RefreshTokenRequest
from .services import UserService
from app.core.dependcies import get_user_service
import jwt

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    user_service: UserService = Depends(get_user_service)
) -> UserSchema:
    try:
        new_user = await user_service.create_user(user)
        return new_user
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )


@router.post("/token", status_code=status.HTTP_201_CREATED)
async def token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service)
):
    try:
        tokens = await user_service.login(form_data.username, form_data.password)
        return tokens
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

@router.post("/access-token", status_code=status.HTTP_200_OK)
async def update_access_token(
    body: RefreshTokenRequest,
    user_service: UserService = Depends(get_user_service)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        new_token = await user_service.update_access_token(body.refresh_token)
        return new_token
    except (InvalidCredentialsError, jwt.PyJWTError):
        raise credentials_exception


@router.post("/refresh-token", status_code=status.HTTP_200_OK)
async def update_refresh_token(
    body: RefreshTokenRequest,
    user_service: UserService = Depends(get_user_service)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        new_token = await user_service.update_refresh_token(body.refresh_token)
        return new_token
    except (InvalidCredentialsError, jwt.PyJWTError):
        raise credentials_exception