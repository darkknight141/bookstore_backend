from typing import List, Annotated

from fastapi import APIRouter, Depends, Query

from api.authors.schemas import (AuthorSchema, ListAuthorSchema, RetrieveAuthorSchema, UpdateAuthorSchema,
                                 FilterAuthorSchema)
from api.authors.services import AuthorService

authors_router = APIRouter(tags=["Authors"])


@authors_router.get('/authors', response_model=List[ListAuthorSchema])
async def get_authors(
        query_params: Annotated[FilterAuthorSchema, Query()],
        service=Depends(AuthorService.from_request)
):
    return await service.list_author(query_params)


@authors_router.get('/authors/{author_id}', response_model=RetrieveAuthorSchema)
async def get_author(author_id: int, service=Depends(AuthorService.from_request)):
    return await service.retrieve_author(author_id)


@authors_router.post('/authors', response_model=RetrieveAuthorSchema, status_code=201)
async def create_author(author: AuthorSchema, service=Depends(AuthorService.from_request)):
    return await service.create_author(author)


@authors_router.patch('/authors/{author_id}', response_model=RetrieveAuthorSchema)
async def update_author(author_id: int, data: UpdateAuthorSchema, service=Depends(AuthorService.from_request)):
    return await service.update_author(author_id, data)


@authors_router.delete('/authors/{author_id}', status_code=204)
async def delete_author(author_id: int, service=Depends(AuthorService.from_request)):
    return await service.delete_author(author_id)
