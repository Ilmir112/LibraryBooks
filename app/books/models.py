from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Books(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year_publication = Column(Integer, nullable=True)
    isbn = Column(String, unique=True, nullable=True)
    count_books = Column(Integer, nullable=False, default=1)
    description = Column(String, nullable=True)

    borrowed_books = relationship("BorrowedBook", back_populates="book")

    def __str__(self):
        return f"Books #{self.id}"
