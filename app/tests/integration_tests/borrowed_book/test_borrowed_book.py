import pytest
from httpx import AsyncClient


def test_one():
    assert 1 == 1


@pytest.mark.parametrize(
    "book_id,reader_id,status_code",
    [
        (1, 1, 200),
        (2, 1, 200),
        (3, 1, 400),
        (3, 2, 200),
        (3, 3, 200),
        (4, 1, 404),
    ],
)
async def test_add_books(
    book_id, reader_id, status_code, authenticated_ac: AsyncClient
):
    response = await authenticated_ac.post(
        "/borrowed_book/issue_book", params={"book_id": book_id, "reader_id": reader_id}
    )
    return response.status_code == status_code


@pytest.mark.parametrize(
    "book_id,reader_id,status_code",
    [(1, 1, 401)],
)
async def test_add_books_not_authenticated(
    book_id, reader_id, status_code, authenticated_ac_not: AsyncClient
):
    response = await authenticated_ac_not.post(
        "/borrowed_book/issue_book", params={"book_id": book_id, "reader_id": reader_id}
    )

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "book_id,reader_id,status_code",
    [
        (1, 1, 200),
        (2, 1, 200),
        (1, 1, 200),
        (1, 1, 200),
    ],
)
async def test_returning_books(
    book_id, reader_id, status_code, authenticated_ac: AsyncClient
):
    response = await authenticated_ac.post(
        "/borrowed_book/returning_books",
        params={"book_id": book_id, "reader_id": reader_id},
    )

    assert response.status_code == status_code
