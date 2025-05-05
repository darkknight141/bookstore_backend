from typing import List

from fastapi import APIRouter, Depends

from api.tags.schemas import (ListTagsSchema, RetrieveTagsSchema, CreateTagsSchema, UpdateTagsSchema,
                              CreateTagBookSchema, RetrieveTagBookSchema)
from api.tags.services import TagsService

tags_router = APIRouter(tags=['Tags'])


@tags_router.get('/tags', response_model=List[ListTagsSchema])
async def get_tags(service=Depends(TagsService.from_request)):
    return await service.list_tags()


@tags_router.get('/tags/{tag_id}', response_model=RetrieveTagsSchema)
async def get_tag(tag_id: int, service=Depends(TagsService.from_request)):
    return await service.retrieve_tag(tag_id)


@tags_router.patch('/tags/{tag_id}', response_model=RetrieveTagsSchema)
async def update_tag(tag_id: int, data: UpdateTagsSchema, service=Depends(TagsService.from_request)):
    return await service.update_tag(tag_id, data)


@tags_router.post('/tags', response_model=RetrieveTagsSchema)
async def create_tag(tag: CreateTagsSchema, service=Depends(TagsService.from_request)):
    return await service.create_tag(tag)


@tags_router.delete('/tags/{tag_id}', response_model=None, status_code=204)
async def delete_tag(tag_id: int, service=Depends(TagsService.from_request)):
    return await service.delete_tag(tag_id)


@tags_router.post('/tags-book', response_model=RetrieveTagBookSchema)
async def add_tag_book(tag_to_book: CreateTagBookSchema, service=Depends(TagsService.from_request)):
    return await service.add_tag_book(tag_to_book)
