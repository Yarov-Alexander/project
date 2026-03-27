import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from starlette import status
from app.core.config import settings
from app.core.dependcies import get_user_service
from app.modules.users.models import User as UserModel
from app.modules.users.services import UserService




oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token:str = Depends(oauth2_scheme), user_service: UserService = Depends(get_user_service)) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="token has expired",
                            headers={"WWW-Authenticate": "Bearer"},
                            )
    except jwt.PyJWTError:
        raise credentials_exception

    user = await user_service.get_user(email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_seller(current_user: UserModel = Depends(get_current_user)):
    if current_user.role != "seller":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Only sellers can perfom actions',
                            headers={"WWW-Authenticate": "Bearer"})
    return current_user

async def get_current_admin(current_user: UserModel = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Only sellers can perfom actions',
                            headers={"WWW-Authenticate": "Bearer"}, )
    return current_user

async def get_current_buyer(current_user: UserModel = Depends(get_current_user)):
    if current_user.role != "buyer":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Only buyers can perfom actions',
                            headers={"WWW-Authenticate": "Bearer"})
    return current_user