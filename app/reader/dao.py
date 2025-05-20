from app.dao.base import BaseDAO
from app.reader.models import Readers


class ReaderDAO(BaseDAO):
    model = Readers
