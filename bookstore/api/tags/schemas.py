from typing import Optional
from pydantic import BaseModel


class TagsSchema(BaseModel):
    name: str


class ListTagsSchema(TagsSchema):
    id: int


class RetrieveTagsSchema(TagsSchema):
    id: int


class CreateTagsSchema(TagsSchema):
    pass


class UpdateTagsSchema(TagsSchema):
    name: Optional['str'] = None


class TagToBookSchema(BaseModel):
    id_book: int
    id_tag: int


class CreateTagBookSchema(TagToBookSchema):
    pass


class RetrieveTagBookSchema(TagToBookSchema):
    id: int
