from app import app

from app.resources.authors.routes import authors_router
from app.resources.categories.routes import categories_router
from app.resources.publishers.routes import publishers_router
from app.resources.books.routes import books_router

app.include_router(authors_router)
app.include_router(categories_router)
app.include_router(publishers_router)
app.include_router(books_router)