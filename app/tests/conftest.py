import json
from datetime import datetime

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import insert

from app.books.models import Books
from app.borrowed_book.models import BorrowedBook
from app.config import settings
from app.database import Base, async_session_maker, engine
from app.main import app as fastapi_app
from app.reader.models import Readers
from app.users.models import Users


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    # Обязательно убеждаемся, что работаем с тестовой БД
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        # Удаление всех заданных нами таблиц из БД
        await conn.run_sync(Base.metadata.drop_all)
        # Добавление всех заданных нами таблиц из БД
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    book = open_mock_json("books")

    readers = open_mock_json("readers")
    users = open_mock_json("users")
    borrowed_books = open_mock_json("borrowed_book")

    for borrowed_book in borrowed_books:
        borrowed_book["borrow_date"] = datetime.strptime(
            borrowed_book["borrow_date"], "%Y-%m-%d"
        )
        if borrowed_book["return_date"]:
            borrowed_book["return_date"] = datetime.strptime(
                borrowed_book["return_date"], "%Y-%m-%d"
            )

    async with async_session_maker() as session:
        for Model, values in [
            (Users, users),
            (Books, book),
            (Readers, readers),
            (BorrowedBook, borrowed_book),
        ]:
            query = insert(Model).values(values)
            await session.execute(query)
        await session.commit()


@pytest.fixture(scope="session")
async def ac():
    "Асинхронный клиент для тестирования эндпоинтов"
    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(scope="session")
async def authenticated_ac():
    "Асинхронный аутентифицированный клиент для тестирования эндпоинтов"
    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app), base_url="http://test"
    ) as ac:
        await ac.post(
            "/auth/login",
            json={"email": "test@test.com", "password": "test"},
        )
        # assert ac.cookies["books_access_token"]
        yield ac


@pytest.fixture(scope="session")
async def authenticated_ac_not():
    "Асинхронный аутентифицированный клиент для тестирования эндпоинтов"
    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app), base_url="http://test"
    ) as ac:
        await ac.post(
            "/auth/login",
            json={"email": "test@test.com", "password": "test1"},
        )
        # assert ac.cookies["books_access_token"]
        yield ac
