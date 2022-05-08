import os
from datetime import timedelta, datetime
from fastapi import Depends
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.auth.exceptions import *

from app.auth.oauth2 import oauth2_scheme
from app.models import User
from app.schemas.schemas import UserInDB, UserRead
from app.services.database import get_db


SECRET_KEY = os.environ.get('SECRET_KEY', 'my_secret_key_123')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    db_user = db.query(User).filter(User.email == username).first()
    if db_user:
        return UserInDB(
            id=db_user.id,
            email=db_user.email,
            is_active=db_user.is_active,
            hashed_password=db_user.hashed_password,
        )


def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(*, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise EXCEPTION_COULD_NOT_VALIDATE

        token_data = TokenData(username=username)

    except JWTError:
        raise EXCEPTION_COULD_NOT_VALIDATE

    user = get_user(db, token_data.username)
    if user is None:
        raise EXCEPTION_COULD_NOT_VALIDATE

    return user


async def get_current_active_user(current_user: UserRead = Depends(get_current_user)):
    if not current_user.is_active:
        raise EXCEPTION_INACTIVE_USER
    return current_user