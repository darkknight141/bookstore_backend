from pydantic import BaseModel


class UserSchema(BaseModel):
    login: str
    password: str


class RetrieveUserSchema(UserSchema):
    id: int

    class Config:
        from_attributes = True


class CreateUserSchema(UserSchema):
    pass


class TokenSchema(BaseModel):
    access_token: str

