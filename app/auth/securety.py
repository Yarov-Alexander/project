from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
import jwt
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
access_expire_token_minutes = 30

def hash_password(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, settings.secret_key, algorithm="HS256")
    return token

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_minutes)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, settings.secret_key, algorithm="HS256")
    return token