from fastapi import APIRouter, Depends, HTTPException, status

from api.exceptions import BaseServiceException
from api.users.schemas import CreateUserSchema, TokenSchema
from api.users.services import UserService

users_router = APIRouter(tags=["Users"])


@users_router.post('/registration', status_code=status.HTTP_204_NO_CONTENT)
async def registration(data: CreateUserSchema, services=Depends(UserService.from_request)):
    try:
        await services.registration(data)
    except BaseServiceException as e:
        HTTPException(status_code=400, detail=str(e))


@users_router.post('/login', response_model=TokenSchema, status_code=200)
async def login(data: CreateUserSchema, services=Depends(UserService.from_request)):
    return await services.login(data)
