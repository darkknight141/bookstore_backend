from typing import Sequence

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from api.tags.schemas import CreateTagsSchema, UpdateTagsSchema, TagToBookSchema
from db.database import get_session
from db.store.models import Tag, TagToBook


class TagsService:
    def __init__(self, session: AsyncSession):
        self.session = session

    @classmethod
    def from_request(cls, session: AsyncSession = Depends(get_session)):
        return cls(session=session)

    async def list_tags(self) -> Sequence[Tag]:
        result = await self.session.execute(select(Tag))
        return result.scalars().all()

    async def retrieve_tag(self, tag_id: int) -> Tag:
        result = await self.session.get(Tag, tag_id)
        return result

    async def create_tag(self, data: CreateTagsSchema) -> Tag:
        tag = Tag(**data.model_dump())
        self.session.add(tag)
        await self.session.commit()
        return tag

    async def update_tag(self, tag_id: int, data: UpdateTagsSchema) -> Tag:
        tag = await self.retrieve_tag(tag_id)
        for key, value in data.model_dump().items():
            setattr(tag, key, value)
        await self.session.commit()
        return tag

    async def delete_tag(self, tag_id: int) -> None:
        tag = await self.retrieve_tag(tag_id)
        if tag:
            await self.session.delete(tag)
            await self.session.commit()

    async def add_tag_book(self, tag_to_book: TagToBookSchema) -> None:
        entity = TagToBook(**tag_to_book.model_dump())
        self.session.add(entity)
        await self.session.commit()
        return entity
