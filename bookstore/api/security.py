import jwt
from fastapi import HTTPException, Depends
from starlette import status
from starlette.requests import Request

from api.users.services import UserService
from settings.config import settings


def get_login(request: Request):
    auth_header = request.headers.get("Authorization")
    if auth_header is None or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    payload = jwt.decode(auth_header.split(' ')[1], settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    login = payload.get('login')
    if not login:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return login


async def verify_token(login=Depends(get_login), user_service=Depends(UserService.from_request)):
    user = await user_service.get_current_user(login=login)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user


