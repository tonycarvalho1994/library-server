from typing import Optional
from pydantic import BaseModel


class BookBase(BaseModel):
    name: str
    description: str = None
    author_id: int
    category_id: int
    publisher_id: int


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    author_id: int = None


class BookRead(BookBase):
    id: int

    class Config:
        orm_mode = True


class SingleAuthorRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class SingleCategoryRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class SinglePublisherRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class BookReadWithAuthor(BaseModel):
    id: int
    name: str
    description: str = None
    author: SingleAuthorRead
    category: SingleCategoryRead
    publisher: SinglePublisherRead

    class Config:
        orm_mode = True


class AuthorBase(BaseModel):
    name: str


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorBase):
    pass


class AuthorRead(AuthorBase):
    id: int
    books: list[BookRead] = []

    class Config:
        orm_mode = True


class CategoryBase(BaseModel):
    name: str
    description: Optional[str]


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int
    books: list[BookRead] = []

    class Config:
        orm_mode = True


class PublisherBase(BaseModel):
    name: str
    description: Optional[str]


class PublisherCreate(PublisherBase):
    pass


class PublisherUpdate(PublisherBase):
    pass


class PublisherRead(PublisherBase):
    id: int
    books: list[BookRead] = []

    class Config:
        orm_mode = True
