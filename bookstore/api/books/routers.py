from typing import List, Annotated

from fastapi import APIRouter, Depends, Query

from api.books.schemas import ListBookSchema, RetrieveBookSchema, CreateBookSchema, UpdateBookSchema, FilterParams
from api.books.services import BookService

books_router = APIRouter(tags=['Books'])


@books_router.get('/books', response_model=List[ListBookSchema])
async def get_books(
        query_params: Annotated[FilterParams, Query()],
        service: BookService = Depends(BookService.from_request)):
    return await service.list_books(query_params)


@books_router.get('/books/{book_id}', response_model=RetrieveBookSchema)
async def get_book(
        book_id: int,
        service: BookService = Depends(BookService.from_request)):
    return await service.retrieve_book(book_id)


@books_router.post('/books', response_model=RetrieveBookSchema)
async def create_book(
        book: CreateBookSchema,
        service: BookService = Depends(BookService.from_request)
):
    return await service.create_book(book)


@books_router.patch('/books/{book_id}', response_model=RetrieveBookSchema)
async def update_book(
        book_id: int,
        book: UpdateBookSchema,
        service: BookService = Depends(BookService.from_request)):
    return await service.update_book(book_id, book)


@books_router.delete('/books/{book_id}', response_model=None, status_code=204)
async def delete_book(
        book_id: int,
        service: BookService = Depends(BookService.from_request)):
    return await service.delete_book(book_id)
