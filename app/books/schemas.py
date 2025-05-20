from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SBooks(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str = Field(..., description="Название книги")
    author: str = Field(..., description="Автор книги")
    year_publication: Optional[int] = Field(None, description="Год публикации")
    isbn: Optional[str] = Field(None,  description="ISBN книги")
    count_books: Optional[int] = Field(1, ge=0, description="Количество экземпляров")
    description: Optional[str] = Field(None,  description="Описание")

    @field_validator("year_publication")
    def check_year_format(cls, v):
        if v is not None:
            if not (1000 <= v <= date.today().year):
                raise ValueError("Год должен быть в формате YYYY")
        return v


class SNewBooks(SBooks):
    model_config = ConfigDict(from_attributes=True)

    title: str
    author: str
    isbn: str | None
    count_books: int | None
