from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    login: str


class UserRetrieveSchema(UserBaseSchema):
    id: int

    class Config:
        from_attributes = True


class UserCreateSchema(UserBaseSchema):
    password: str


class UserLoginSchema(UserBaseSchema):
    password: str


class TokenSchema(BaseModel):
    access_token: str

