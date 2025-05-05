from fastapi import FastAPI

from api.books.routers import books_router
from api.authors.routers import authors_router
from api.tags.routers import tags_router
from api.users.routers import users_router
from api.carts.routers import carts_router

app = FastAPI()

app.include_router(books_router)
app.include_router(authors_router)
app.include_router(tags_router)
app.include_router(users_router)
app.include_router(carts_router)

