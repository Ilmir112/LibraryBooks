import pytest
from httpx import AsyncClient


def test_one():
    assert 1 == 1


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("Maksim@mail.com", "qwerty", 201),
        ("Maksim@mail.com", "qwerty1", 409),
        ("Alex@mail.com", "qwerty", 201),
        ("abcde", "1953", 422),
    ],
)
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("Maksim@mail.com", "qwerty", 200),
        ("wrong@person.com", "qwerty", 401),
    ],
)
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == status_code
