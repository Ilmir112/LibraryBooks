from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from app.exceptions import (
    CannotUpdateDataToDatabase,
    MultipleDataToDatabase,
    ReadersDeleteToDatabase,
    UpdateDataToDatabase,
)
from app.reader.dao import ReaderDAO
from app.reader.schemas import SNewReader, SReaders
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/readers",
    tags=["Читатели"],
)


@router.post("/add_reader", status_code=201)
async def add_book(
        reader: SReaders = Depends(), user: Users = Depends(get_current_user)
):
    existing = await ReaderDAO.find_one_or_none(email=reader.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email должен быть уникальным")

    await ReaderDAO.add(name=reader.name, email=reader.email)
    return HTTPException(status_code=200, detail=f"читатель - {reader.name} добавлен ")


#
@router.get("/all_reader")
async def get_all_books(user: Users = Depends(get_current_user)):
    if user:
        return await ReaderDAO.find_all()


@router.get("/find_one_reader")
async def get_one_reader(
        name: Optional[str] = None,
        email: Optional[str] = None,
        user: Users = Depends(get_current_user),
):
    if name and email:
        return await ReaderDAO.find_one_or_none(name=name, email=email)
    elif name is None and email:
        return await ReaderDAO.find_one_or_none(email=email)
    elif name and email is None:
        result = await ReaderDAO.find_one_or_none(name=name)
        if result:
            return result
        else:
            raise MultipleDataToDatabase


@router.put("/update_readers")
async def update_reader_data(
        reader_new: SNewReader,
        reader: SReaders = Depends(get_one_reader),
        current_user: Users = Depends(get_current_user),
):
    if reader:
        new_data = await ReaderDAO.update_data(
            reader.id, name=reader_new.name, email=reader_new.email
        )
        if not new_data:
            raise CannotUpdateDataToDatabase
        raise UpdateDataToDatabase

    else:
        raise MultipleDataToDatabase


@router.delete("/delete")
async def delete_reader(
        current_user: Users = Depends(get_current_user), reader: SNewReader = Depends()
):
    if reader:
        await ReaderDAO.delete(name=reader.name, email=reader.email)
        raise ReadersDeleteToDatabase
