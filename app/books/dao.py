from app.books.models import Books
from app.dao.base import BaseDAO


class BookDAO(BaseDAO):
    model = Books
