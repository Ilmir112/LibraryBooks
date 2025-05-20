import pytest
from httpx import AsyncClient

from app.books.dao import BookDAO


def test_one():
    assert 1 == 1


@pytest.mark.parametrize(
    "title,author,year_publication,isbn,count_books",
    [
        ("Книга23", "Авто1р", 2020, "125-254", 20),
        ("Книга", "Автор", 2024, "1254-45125-125", 20),
        ("Книга2", "Автор2", 2020, "1254-45125-125-251", 3),
        ("Книга3", "Автор4", None, "1254-45125-125-25", 3),
    ],
)
async def test_add_books(
        title, author, year_publication, isbn, count_books,
        authenticated_ac: AsyncClient
):
    new_book = await BookDAO.add(
        title=title,
        author=author,
        year_publication=year_publication,
        isbn=isbn,
        count_books=count_books,
    )

    new_book = await BookDAO.find_one_or_none(id=new_book.id)
    assert new_book is not None

    new_data = await BookDAO.update_data(new_book, title="Книга25")
    assert new_data["title"] == "Книга25"

    # Удаление
    await BookDAO.delete(id=new_book["id"])
    new_book = await BookDAO.find_one_or_none(id=new_book.id)
    assert new_book is None
