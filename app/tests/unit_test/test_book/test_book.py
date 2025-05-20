import pytest

from app.books.dao import BookDAO


@pytest.mark.parametrize(
    "book_id,title,is_present",
    [
        (1, "Книга2", True),
        (30, "Книга30", False),
    ],
)
async def test_find_book_by_isbn(book_id, title, is_present):
    book = await BookDAO.find_one_or_none(id=book_id)
    if is_present:
        assert book
        assert book["id"] == book_id

    else:
        assert not book
