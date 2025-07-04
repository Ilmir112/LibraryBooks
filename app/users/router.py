from fastapi import APIRouter, Depends, Response

from app.exceptions import (
    CannotAddDataToDatabase,
    CannotUpdateDataToDatabase,
    UpdateDataToDatabase,
    UpdateNotDataToDatabase,
    UserAlreadyExistsException,
)
from app.users.auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.users.dao import UserDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.schemas import SUserAuth

router_auth = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

router_users = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
)


@router_auth.post("/register", status_code=201)
async def register_user(user_data: SUserAuth):
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    new_user = await UserDAO.add(email=user_data.email, hashed_password=hashed_password)
    if not new_user:
        raise CannotAddDataToDatabase


@router_auth.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("library_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router_auth.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("library_access_token")


@router_users.get("/all_users")
async def read_users_all(current_user: Users = Depends(get_current_user)):
    if current_user:
        result = await UserDAO.find_all()
        return result


@router_users.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user


@router_users.put("/update")
async def update_user_data(
    user_data: SUserAuth, current_user: Users = Depends(get_current_user)
):

    if (
        verify_password(user_data.password, current_user.hashed_password)
        and user_data.email == current_user.email
    ):
        raise UpdateNotDataToDatabase
    hashed_password = get_password_hash(user_data.password)

    new_user_data = await UserDAO.update_data(
        current_user, email=user_data.email, hashed_password=hashed_password
    )
    if not new_user_data:
        raise CannotUpdateDataToDatabase
    raise UpdateDataToDatabase


@router_users.post("/delete")
async def delete_current_user(current_user: Users = Depends(get_current_user)):
    await UserDAO.delete(id=current_user.id)
