from typing import Sequence, Self

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_session
from db.store.models import Author
from api.authors.schemas import UpdateAuthorSchema, CreateAuthorSchema


class AuthorService:
    def __init__(self, session: AsyncSession):
        self.session = session

    @classmethod
    def from_request(cls, session: AsyncSession = Depends(get_session)) -> Self:
        return cls(session=session)

    async def list_author(self) -> Sequence[Author]:
        result = await self.session.execute(select(Author))
        return result.scalars().all()

    async def retrieve_author(self, author_id: int) -> Author:
        result = await self.session.get(Author, author_id)
        return result

    async def create_author(self, data: CreateAuthorSchema) -> Author:
        author = Author(
            first_name=data.first_name,
            last_name=data.last_name,
            middle_name=data.middle_name,
            born_year=data.born_year,
            country=data.country
        )
        self.session.add(author)
        await self.session.commit()
        return author

    async def update_author(self, author_id: int, data: UpdateAuthorSchema) -> Author:
        author = await self.retrieve_author(author_id)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(author, key, value)
        await self.session.commit()
        return author

    async def delete_author(self, author_id: int) -> None:
        author = await self.retrieve_author(author_id)
        if author:
            await self.session.delete(author)
            await self.session.commit()
