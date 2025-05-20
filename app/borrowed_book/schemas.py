from datetime import date

from pydantic import BaseModel, ConfigDict


class SBorrowRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    book_id: int
    reader_id: int
    borrow_date: date
    return_date: date | None
