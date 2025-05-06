from fastapi import APIRouter, Depends, status

from api.users.schemas import CreateUserSchema, TokenSchema
from api.users.services import UserService

users_router = APIRouter(tags=["Users"])


@users_router.post('/register', status_code=status.HTTP_204_NO_CONTENT)
async def register_user(
        data: CreateUserSchema,
        services: UserService = Depends(UserService.from_request)
):
    await services.registration(data)


@users_router.post('/login', response_model=TokenSchema, status_code=200)
async def login_user(
        data: CreateUserSchema,
        services: UserService = Depends(UserService.from_request)
):
    return await services.login(data)
