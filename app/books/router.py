from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from app.books.dao import BookDAO
from app.books.schemas import SBooks, SNewBooks
from app.exceptions import (
    BooksCannotBeBooked,
    BooksDeleteToDatabase,
    CannotUpdateDataToDatabase,
    UpdateDataToDatabase,
)
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/books",
    tags=["Книги"],
)


class BooksSearchArgs:
    def __init__(
            self,
            title: Optional[str] = None,
            author: Optional[str] = None,
            isbn: Optional[str] = None,
            year_publication: Optional[int] = None,
    ):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.year_publication = year_publication
        if self.title:
            self.title.lower()
        if self.author:
            self.author.lower()


@router.post("/add_books", status_code=201)
async def add_book(books: SBooks = Depends(), user: Users = Depends(get_current_user)):
    existing = await BookDAO.find_one_or_none(isbn=books.isbn)
    if existing:
        raise HTTPException(status_code=400, detail="ISBN must be unique")

    books = await BookDAO.add(
        title=books.title,
        author=books.author,
        year_publication=books.year_publication,
        isbn=books.isbn,
        count_books=books.count_books,
        description=books.description
    )
    if not books:
        raise BooksCannotBeBooked

    return books


#
@router.get("/all_books")
async def get_all_books(user: Users = Depends(get_current_user)):
    return await BookDAO.find_all()


@router.get("/find_one_book")
async def get_one_book(
        title: str, author: str, user: Users = Depends(get_current_user)
):
    return await BookDAO.find_one_or_none(title=title, author=author)


@router.put("/update_books")
async def update_book_data(
        books_new: SBooks,
        books: BooksSearchArgs = Depends(get_one_book),
        current_user: Users = Depends(get_current_user),
):
    if books:
        new_data = await BookDAO.update_data(
            books,
            title=books_new.title,
            author=books_new.author,
            year_publication=books_new.year_publication,
            isbn=books_new.isbn,
            count_books=books_new.count_books,
        )
        if not new_data:
            raise CannotUpdateDataToDatabase
        raise UpdateDataToDatabase


@router.delete("/delete")
async def delete_book(
        current_user: Users = Depends(get_current_user), books_id: SNewBooks = Depends()
):
    if current_user and books_id:
        await BookDAO.delete(id=current_user.id)
        return BooksDeleteToDatabase
