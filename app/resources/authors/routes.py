from fastapi import Depends, APIRouter, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.schemas.schemas import AuthorCreate, AuthorRead, AuthorUpdate
from app.models import Author
from app.services.database import get_db
from app.resources import Tags


authors_router = APIRouter(prefix='/authors')


@authors_router.post(
    '/', 
    response_model=AuthorRead, 
    response_model_exclude_none=True, 
    status_code=status.HTTP_201_CREATED,
    tags=[Tags.Authors]
)
def create_author(*, db: Session = Depends(get_db), author: AuthorCreate):
    try:
        new_author = Author(name=author.name)
        db.add(new_author)
        db.commit()
        db.refresh(new_author)

        return new_author
    except IntegrityError:
        db.rollback()
        db.close()
        raise HTTPException(status_code=400, detail="Author already exists.")


@authors_router.get(
    '/{author_id}', 
    response_model=AuthorRead, 
    response_model_exclude_none=True,
    tags=[Tags.Authors]
)
def get_author_by_id(*, db: Session = Depends(get_db), author_id: int):
    author = db.query(Author).filter(Author.id == author_id).first()

    if not author:
        raise HTTPException(status_code=404, detail="Author not found.")

    return author


@authors_router.get(
    '/', 
    response_model=list[AuthorRead], 
    response_model_exclude_none=True,
    tags=[Tags.Authors]
)
def get_all_authors(
    *, 
    db: Session = Depends(get_db), 
    name: str | None = Query(None, min_length=3, max_length=20)
):
    if name:
        return db.query(Author).filter(Author.name.ilike('%' + name + '%')).all()
    
    return db.query(Author).all()


@authors_router.patch(
    '/{author_id}', 
    response_model=AuthorRead, 
    response_model_exclude_none=True,
    tags=[Tags.Authors]
)
def update_author(*, db: Session = Depends(get_db), author_id: int, author: AuthorUpdate):
    db_author = db.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    author_data = author.dict(exclude_unset=True)
    for key, value in author_data.items():
            setattr(db_author, key, value)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


@authors_router.delete('/{author_id}', tags=[Tags.Authors])
def delete_author(*, db: Session = Depends(get_db), author_id: int):
    author = db.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    db.delete(author)
    db.commit()
    return {'ok': True}
