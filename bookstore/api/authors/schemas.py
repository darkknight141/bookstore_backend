import datetime
from typing import Optional

from pydantic import BaseModel, Field


class AuthorSchema(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    born_year: datetime.date
    country: str


class ListAuthorSchema(AuthorSchema):
    id: int

    class Config:
        from_attributes = True


class RetrieveAuthorSchema(AuthorSchema):
    id: int

    class Config:
        from_attributes = True


class CreateAuthorSchema(AuthorSchema):
    pass


class UpdateAuthorSchema(AuthorSchema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    born_year: Optional[datetime.date] = None
    country: Optional[str] = None


class FilterAuthorSchema(BaseModel):
    born_year: int = Field(None)
