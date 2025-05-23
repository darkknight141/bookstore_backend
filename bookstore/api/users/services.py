from datetime import datetime, timedelta, timezone
from typing import Self

import jwt
from fastapi import Depends, HTTPException
from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from starlette import status

from api.users.schemas import UserCreateSchema
from db.database import get_session
from db.store.models import User
from settings.config import settings

from bookstore.api.exceptions import ClientException


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def from_request(cls, session: AsyncSession = Depends(get_session)) -> Self:
        return cls(session)

    async def registration(self, data: UserCreateSchema) -> None:
        is_exist = await self._validate_login(data.model_dump()['login'])
        if is_exist:
            raise ClientException(detail="Пользователь уже создан")
        hash_password = self._hash_password(data.model_dump()['password'])
        user = User(login=data.model_dump()['login'], password=hash_password)
        self.session.add(user)
        await self.session.commit()

    async def login(self, data: UserCreateSchema) -> dict[str, str]:
        user = await self.session.execute(select(User).where(User.login == data.model_dump()['login']))
        user = user.scalar()
        if not user:
            raise ClientException(detail="Некорректный логин")
        is_verify_password = self._verify_password(data.model_dump()['password'], user.password)
        if not is_verify_password:
            raise ClientException(detail="Некорректный пароль")
        access_token = self._create_access_token(data)
        return {'access_token': access_token}

    def _hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def _verify_password(self, password: str, hashed_password: str) -> bool:
        return bool(self.pwd_context.verify(password, hashed_password))

    @staticmethod
    def _create_access_token(user) -> str:
        to_encode = user.model_dump().copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.TTL_ACCESS_TOKEN_MINUTES)
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    async def _validate_login(self, login: str) -> bool:
        exist_user = await self.session.execute(select(exists().where(User.login == login)))
        exist_user = exist_user.scalar()
        return exist_user

    async def get_current_user(self, login: str) -> User:
        user = await self.session.execute(select(User).where(User.login == login))
        user = user.scalar()
        return user

