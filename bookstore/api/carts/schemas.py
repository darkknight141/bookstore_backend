from typing import List, Optional

from pydantic import BaseModel


class CartItemSchema(BaseModel):
    id_book: int
    count_book: int
    price: int


class CartSchema(BaseModel):
    id_user: int
    items: List[CartItemSchema]


class CreateCartItemSchema(BaseModel):
    book_id: int
    count_book: int


class RetrieveCart(CartSchema):

    class Config:
        from_attributes = True


class UpdateCartItemSchema(BaseModel):
    count_book: Optional[int] = None


class AddedBookFromCartSchema(BaseModel):
    id_user: int
    id_book: int
    count_book: int

    class Config:
        from_attributes = True


