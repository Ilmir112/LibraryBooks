from sqlalchemy import Column, Date, ForeignKey, Integer, func
from sqlalchemy.orm import relationship

from app.database import Base


class BorrowedBook(Base):
    __tablename__ = "borrowed_books"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    reader_id = Column(Integer, ForeignKey("readers.id"), nullable=False)
    borrow_date = Column(Date, default=func.now(), nullable=False)
    return_date = Column(Date, nullable=True)

    book = relationship("Books", back_populates="borrowed_books")
    reader = relationship("Readers", back_populates="borrowed_books")

    def __str__(self):
        return f"Reader #{self.id}"
