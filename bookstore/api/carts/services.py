from typing import Self

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.carts.schemas import CreateCart, UpdateCart, RetrieveCart, BooksInCartSchema
from db.database import get_session
from db.store.models import Cart, User


class CartsService:
    def __init__(self, session):
        self.session = session

    @classmethod
    def from_request(cls, session: AsyncSession = Depends(get_session)) -> Self:
        return cls(session=session)

    async def get_cart(self, user: User) -> RetrieveCart:
        carts = await self.session.execute(select(Cart).where(Cart.id_user == user.id))
        carts = carts.scalars().all()
        books_in_cart = [
            BooksInCartSchema(id_book=cart.id_book, count_book=cart.count_book, price=cart.book.price)
            for cart in carts
        ]
        return RetrieveCart(
            id_user=user.id,
            items=books_in_cart
        )

    async def add_book_to_cart(self, cart_data: CreateCart, user: User) -> Cart:
        cart_data = cart_data.model_dump()
        new_cart = Cart(
            id_user=user.id,
            id_books=cart_data['book_id'],
            count_book=cart_data['count_book'],
        )
        self.session.add(new_cart)
        await self.session.commit()
        return new_cart

    async def update_book_from_cart(self, book_id: int, user: User, cart_data: UpdateCart) -> RetrieveCart:
        cart_data = cart_data.model_dump(exclude_unset=True)
        item = await self.session.execute(select(Cart).where(Cart.id_user == user.id, Cart.id_books == book_id))
        item = item.scalar()
        for key, value in cart_data.items():
            setattr(item, key, value)
        await self.session.commit()
        result = await self.get_cart(user)
        books_in_cart = [
            BooksInCartSchema(id_book=cart.id_book, count_book=cart.count_book) for cart in result]
        return RetrieveCart(
            id_user=user.id,
            items=books_in_cart
        )

    async def delete_book_from_cart(self, book_id: int, user: User) -> None:
        item = await self.session.execute(select(Cart).where(Cart.id_user == user.id, Cart.id_books == book_id))
        if item:
            await self.session.delete(item)
            await self.session.commit()



