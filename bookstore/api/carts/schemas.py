from typing import List, Optional

from pydantic import BaseModel


class BooksInCartSchema(BaseModel):
    id_book: int
    count_book: int
    price: int


class CartsSchema(BaseModel):
    id_user: int
    items: List[BooksInCartSchema]


class CreateCart(BaseModel):
    book_id: int
    count_book: int


class RetrieveCart(CartsSchema):

    class Config:
        from_attributes = True


class UpdateCart(CreateCart):
    count_book: Optional[int] = None


class GetAddedBookFromCart(BaseModel):
    id_user: int
    id_books: int
    count_book: int

    class Config:
        from_attributes = True


