from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.services.database import Base


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    books = relationship('Book', back_populates='author')


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    author_id = Column(Integer, ForeignKey('authors.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    publisher_id = Column(Integer, ForeignKey('publishers.id'))

    author = relationship('Author', back_populates='books')
    category = relationship('Category', back_populates='books')
    publisher = relationship('Publisher', back_populates='books')


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)

    books = relationship('Book', back_populates='category')


class Publisher(Base):
    __tablename__ = 'publishers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)

    books = relationship('Book', back_populates='publisher')
