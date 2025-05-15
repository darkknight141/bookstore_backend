import datetime
from typing import Optional

from pydantic import BaseModel, Field, ValidationError, field_validator


class BookSchema(BaseModel):
    title: str
    description: str
    year_created: int
    image: bytes
    id_author: int
    price: int


class ListBookSchema(BaseModel):
    id: int
    title: str
    description: str

    class Config:
        from_attributes = True


class RetrieveBookSchema(BookSchema):
    id: int

    class Config:
        from_attributes = True


class CreateBookSchema(BookSchema):
    pass

    @classmethod
    @field_validator('year_created')
    def validate_year_created(cls, year_created: int):
        if year_created > datetime.datetime.now().year:
            raise ValidationError("Year must be less than current year")
        return year_created


class UpdateBookSchema(BookSchema):
    title: Optional[str] = None
    description: Optional[str] = None
    year_created: Optional[datetime.datetime] = None
    image: Optional[bytes] = None
    id_author: Optional[int] = None


class FilterParams(BaseModel):
    year_created: int = Field(None)
    id_author: int = Field(None)
    tag: int = Field(None)







