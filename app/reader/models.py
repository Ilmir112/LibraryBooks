from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Readers(Base):
    __tablename__ = "readers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String(50), unique=True, nullable=False)

    borrowed_books = relationship("BorrowedBook", back_populates="reader")

    def __str__(self):
        return f"Reader #{self.id}"
