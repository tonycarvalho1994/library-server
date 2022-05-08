from typing import List
from fastapi import Depends, APIRouter, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.schemas.schemas import BookCreate, BookReadWithAuthor, BookUpdate
from app.auth.oauth2 import oauth2_scheme
from app.services.database import get_db
from app.resources import Tags
from app.models import Author, Book, Category, Publisher


books_router = APIRouter(prefix='/books')


@books_router.post(
    '/', 
    response_model=BookReadWithAuthor, 
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    tags=[Tags.Books],
    dependencies=[Depends(oauth2_scheme)]
)
def create_book(*, db: Session = Depends(get_db), book: BookCreate):
    db_book = db.query(Book).filter(Book.name == book.name).first()
    if db_book:
        raise HTTPException(status_code=400, detail="Book already exists.")

    db_author = db.query(Author).filter(Author.id == book.author_id).first()
    if not db_author:
        raise HTTPException(status_code=400, detail="Author not found.")

    db_category = db.query(Category).filter(Category.id == book.category_id).first()
    if not db_category:
        raise HTTPException(status_code=400, detail="Category not found.")

    db_publisher = db.query(Publisher).filter(Publisher.id == book.publisher_id).first()
    if not db_publisher:
        raise HTTPException(status_code=400, detail="Publisher not found.")

    try:
        new_book = Book(
            name=book.name, 
            description=book.description, 
            author_id=book.author_id,
            category_id=book.category_id,
            publisher_id=book.publisher_id,
        )
        db.add(new_book)
        db.commit()
        db.refresh(new_book)

        return new_book
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Something went wrong.")

@books_router.get(
    '/{book_id}', 
    response_model=BookReadWithAuthor, 
    response_model_exclude_none=True,
    tags=[Tags.Books]
)
def get_book_by_id(*, db: Session = Depends(get_db), book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")

    return book


@books_router.get(
    '/', 
    response_model=List[BookReadWithAuthor], 
    response_model_exclude_none=True,
    tags=[Tags.Books]
)
def get_all_books(
    *, db: Session = Depends(get_db), 
    name: str | None = Query(None, min_length=3, max_length=20),
    author_id: int | None = Query(None),
    category_id: int | None = Query(None),
    publisher_id: int | None = Query(None),
):
    base_query = db.query(Book)
    if name:
        base_query = base_query.filter(Book.name.ilike('%' + name + '%'))

    if author_id:
        base_query = base_query.filter(Book.author_id == author_id)

    if category_id:
        base_query = base_query.filter(Book.category_id == category_id)

    if publisher_id:
        base_query = base_query.filter(Book.publisher_id == publisher_id)

    return base_query.all()


@books_router.patch(
    '/{book_id}', 
    response_model=BookReadWithAuthor, 
    response_model_exclude_none=True,
    tags=[Tags.Books],
    dependencies=[Depends(oauth2_scheme)]
)
def update_book(*, db: Session = Depends(get_db), book_id: int, book: BookUpdate):
    db_book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    book_data = book.dict(exclude_unset=True)
    for key, value in book_data.items():
            setattr(db_book, key, value)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@books_router.delete('/{book_id}', tags=[Tags.Books], dependencies=[Depends(oauth2_scheme)])
def delete_book(*, db: Session = Depends(get_db), book_id: int):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(book)
    db.commit()
    return {'ok': True}
