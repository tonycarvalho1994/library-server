from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.authentication import get_current_active_user, get_password_hash
from app.models import User
from app.resources import Tags
from app.schemas.schemas import UserCreate, UserRead
from app.services.database import get_db


users_router = APIRouter(prefix='/users')


@users_router.get('/me/', response_model=UserRead, tags=[Tags.Users])
async def read_users_me(current_user: UserRead = Depends(get_current_active_user)):
    return current_user


@users_router.post('/', tags=[Tags.Users], status_code=status.HTTP_201_CREATED,)
def create_user(*, db: Session = Depends(get_db), user: UserCreate):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail='Email already exists')
    
    new_user = User(
        email=user.email,
        hashed_password=get_password_hash(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {'ok': True}
