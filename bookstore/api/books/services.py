from typing import Sequence, Self

from fastapi import Depends
from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from bookstore.api.exceptions import NotFoundException
from db.database import get_session
from db.store.models import Book, Author
from api.books.schemas import CreateBookSchema, UpdateBookSchema, FilterParams


class BookService:
    def __init__(self, session: AsyncSession):
        self.session = session

    @classmethod
    def from_request(cls, session: AsyncSession = Depends(get_session)) -> Self:
        return cls(session=session)

    async def list_books(self, query_params: FilterParams) -> Sequence[Book]:
        query = select(Book)
        if query_params:
            for key, value in query_params.model_dump(exclude_unset=True).items():
                query = query.where(getattr(Book, key) == value)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def retrieve_book(self, book_id: int) -> Book:
        result = await self.session.get(Book, book_id)
        return result

    async def create_book(self, data: CreateBookSchema) -> Book:
        exists_author = await self._validate_author(data.model_dump()['id_author'])
        if not exists_author:
            raise NotFoundException("Автор не найден")
        book = Book(**data.model_dump())
        self.session.add(book)
        await self.session.commit()
        return book

    async def update_book(self, book_id: int, data: UpdateBookSchema) -> Book:
        book = await self.retrieve_book(book_id)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(book, key, value)
        await self.session.commit()
        return book

    async def delete_book(self, book_id: int) -> None:
        book = await self.retrieve_book(book_id)
        if book:
            await self.session.delete(book)
            await self.session.commit()

    async def _validate_author(self, author_id: int) -> bool:
        exist_author = await self.session.execute(select(exists().where(Author.id == author_id)))
        exist_author = exist_author.scalar()
        return exist_author