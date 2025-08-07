from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.books.dao import BookDAO
from app.borrowed_book.dao import BorrowedDAO
from app.exceptions import (
    BooksCancelException,
    BooksCannotNullBeBooked,
    FindBookAndReaderException,
    FindBorrowedBookAndReaderException,
    FindNotBooksException,
    FindReaderException,
    ReadersNotBorrowedBookException,
)
from app.logger import logger
from app.reader.dao import ReaderDAO
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/borrowed_book",
    tags=["Выдача книг"],
)


@router.get("/all_borrowed_book")
async def get_all_books(user: Users = Depends(get_current_user)):
    try:
        if user:
            return await BorrowedDAO.find_all()
    except SQLAlchemyError as db_err:
        msg = f"Database Exception update reader {db_err}"
        logger.error(msg, exc_info=True, extra={"user": user})
        raise HTTPException(status_code=500, detail=msg)
    except Exception as e:
        msg = f"Unexpected error: {str(e)}"
        logger.error(msg, exc_info=True, extra={"user": user})
        raise HTTPException(status_code=500, detail=msg)


@router.get("/all_borrowed_book_not_returned")
async def get_all_borrowed_book_not_returned(
    reader_id: int, current_user: Users = Depends(get_current_user)
):
    try:
        active_borrows = await BorrowedDAO.find_all(
            reader_id=reader_id, return_date=None
        )
        if active_borrows:
            return active_borrows
        else:
            return ReadersNotBorrowedBookException
    except SQLAlchemyError as db_err:
        msg = f"Database Exception update reader {db_err}"
        logger.error(msg, exc_info=True, extra={"user": current_user})
        raise HTTPException(status_code=500, detail=msg)
    except Exception as e:
        msg = f"Unexpected error: {str(e)}"
        logger.error(msg, exc_info=True, extra={"user": current_user})
        raise HTTPException(status_code=500, detail=msg)


@router.post("/issue_book")
async def issue_book(
    book_id: int, reader_id: int, current_user=Depends(get_current_user)
):
    try:
        book = await BookDAO.find_one_or_none(id=book_id)
        if not book:
            return FindNotBooksException
        if book["count_books"] <= 0:
            return BooksCancelException

        reader = await ReaderDAO.find_one_or_none(id=reader_id)
        if not reader:
            return FindReaderException

        if reader:
            count_book = await BorrowedDAO.find_all(
                reader_id=reader_id, return_date=None
            )
            if len(count_book) >= 3:
                return FindBookAndReaderException

            date_borrow = datetime.now()

            # Выдача книги
            borrowed = await BorrowedDAO.add(
                book_id=book_id,
                reader_id=reader_id,
                borrow_date=date_borrow,
                return_date=None,
            )
            if borrowed:
                new_data = await BookDAO.update_data(
                    book, count_books=book["count_books"] - 1
                )
                if new_data:
                    return {
                        "message": "Книга выдана успешно",
                        "borrow_id": borrowed.id,
                        "copy_book": new_data.count_books,
                    }
        else:
            return FindBorrowedBookAndReaderException
    except SQLAlchemyError as db_err:
        msg = f"Database Exception update reader {db_err}"
        logger.error(msg, exc_info=True, extra={"user": current_user})
        raise HTTPException(status_code=500, detail=msg)
    except Exception as e:
        msg = f"Unexpected error: {str(e)}"
        logger.error(msg, exc_info=True, extra={"user": current_user})
        raise HTTPException(status_code=500, detail=msg)


@router.post("/returning_books")
async def returning_books(
    book_id: int, reader_id: int, current_user=Depends(get_current_user)
):
    try:
        borrowed = await BorrowedDAO.find_all(
            book_id=book_id, reader_id=reader_id, return_date=None
        )

        if borrowed:
            if len(borrowed) >= 1:
                borrowed = borrowed[0]

            book = await BookDAO.find_one_or_none(id=book_id)

            if borrowed:
                date_returning = datetime.now()
                new_data = await BorrowedDAO.update_data(
                    borrowed, return_date=date_returning
                )
                if new_data:
                    new_data = await BookDAO.update_data(
                        book, count_books=book["count_books"] + 1
                    )

                    return {
                        "message": "Книга выдана сдана",
                        "copy_book": new_data["count_books"],
                    }
        else:
            return BooksCannotNullBeBooked
    except SQLAlchemyError as db_err:
        msg = f"Database Exception update reader {db_err}"
        logger.error(msg, exc_info=True, extra={"user": current_user})
        raise HTTPException(status_code=500, detail=msg)
    except Exception as e:
        msg = f"Unexpected error: {str(e)}"
        logger.error(msg, exc_info=True, extra={"user": current_user})
        raise HTTPException(status_code=500, detail=msg)
