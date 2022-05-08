from datetime import timedelta
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.resources import Tags

from app.services.database import get_db
from app.auth.authentication import (
    ACCESS_TOKEN_EXPIRE_MINUTES, 
    authenticate_user, 
    create_access_token,
)
from app.auth.exceptions import EXCEPTION_INCORRECT_USER_OR_PASSWORD

auth_router = APIRouter()


@auth_router.post('/token', tags=[Tags.Auth])
async def login_for_access_token(*, db: Session = Depends(get_db),form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise EXCEPTION_INCORRECT_USER_OR_PASSWORD

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}