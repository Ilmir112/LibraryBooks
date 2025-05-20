from sqlalchemy import Column, Integer, String

from app.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    email = Column(String, nullable=False, primary_key=True)
    hashed_password = Column(String, nullable=False)

    def __str__(self):
        return f"Пользователь {self.email}"
