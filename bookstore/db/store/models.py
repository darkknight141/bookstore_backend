from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bookstore.db.database import Base, int_pk, str_null_true


class Book(Base):
    id: Mapped[int_pk]
    title: Mapped[str_null_true]
    description: Mapped[str_null_true]
    year_created: Mapped[int] = mapped_column(nullable=True)
    image: Mapped[Optional[bytes]] = mapped_column(LargeBinary, nullable=True)
    id_author: Mapped[int] = mapped_column(ForeignKey('authors.id'), nullable=False)
    author: Mapped['Author'] = relationship('Author', backref='books')

    def __str__(self) -> str:
        return (
            f'{self.__class__.__name__} {self.id}'
            f'{self.title}'
        )

    def __repr__(self) -> str:
        return str(self)


class Author(Base):
    id: Mapped[int_pk]
    first_name: Mapped[str_null_true]
    last_name: Mapped[str_null_true]
    middle_name: Mapped[str_null_true]
    born_year: Mapped[datetime]
    country: Mapped[str_null_true]

    def __str__(self) -> str:
        return (
            f'{self.__class__.__name__} {self.id}'
            f'{self.first_name} {self.last_name}'
        )

    def __repr__(self) -> str:
        return str(self)


class User(Base):
    id: Mapped[int_pk]
    login: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.id}'

    def __repr__(self) -> str:
        return str(self)


class Cart(Base):
    id: Mapped[int_pk]
    id_user: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    id_books: Mapped[int] = mapped_column(ForeignKey('books.id'), nullable=False)
    count_book: Mapped[int]
    user: Mapped[User] = relationship('User', backref='carts_book')
    book: Mapped[Book] = relationship('Book', backref='carts_user')

    def __str__(self) -> str:
        return (
            f'{self.__class__.__name__} {self.id}'
            f'{self.id_user} | {self.id_books} | {self.count_book}'
        )

    def __repr__(self) -> str:
        return str(self)


class Tag(Base):
    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(nullable=False)

    def __str__(self) -> str:
        return (
            f'{self.__class__.__name__} {self.id}'
            f'{self.name}'
        )

    def __repr__(self) -> str:
        return str(self)


class TagToBook(Base):
    id: Mapped[int_pk]
    id_book: Mapped[int] = mapped_column(ForeignKey('books.id'), nullable=False)
    id_tag: Mapped[int] = mapped_column(ForeignKey('tags.id'), nullable=False)
    book: Mapped[Book] = relationship('Book', backref='tags_book')
    tag: Mapped[Tag] = relationship('Tag', backref='tags_user')

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.id}'

    def __repr__(self) -> str:
        return str(self)
