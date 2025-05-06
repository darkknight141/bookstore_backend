from fastapi import FastAPI

from api.books.routers import books_router
from api.authors.routers import authors_router
from api.tags.routers import tags_router
from api.users.routers import users_router
from api.carts.routers import carts_router
from starlette.requests import Request
from starlette.responses import JSONResponse

from bookstore.api.exceptions import BaseServiceException

app = FastAPI()


@app.exception_handler(BaseServiceException)
async def http_exception_handler(request: Request, exc: BaseServiceException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


app.include_router(books_router)
app.include_router(authors_router)
app.include_router(tags_router)
app.include_router(users_router)
app.include_router(carts_router)
