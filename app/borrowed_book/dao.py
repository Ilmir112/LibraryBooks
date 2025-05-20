from app.borrowed_book.models import BorrowedBook
from app.dao.base import BaseDAO


class BorrowedDAO(BaseDAO):
    model = BorrowedBook
