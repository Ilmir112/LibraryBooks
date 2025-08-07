from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.exceptions import (
    CannotUpdateDataToDatabase,
    MultipleDataToDatabase,
    ReadersDeleteToDatabase,
    UpdateDataToDatabase,
    UserAlreadyExistsException,
)
from app.logger import logger
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
    try:
        existing = await ReaderDAO.find_one_or_none(email=reader.email)
        if existing:
            raise UserAlreadyExistsException

        await ReaderDAO.add(name=reader.name, email=reader.email)
        return HTTPException(
            status_code=200, detail=f"читатель - {reader.name} добавлен "
        )
    except SQLAlchemyError as db_err:
        msg = f"Database Exception add book {db_err}"
        logger.error(
            msg,
            extra={"reader": reader},
            exc_info=True,
        )
    except Exception as e:
        msg = f"Unexpected error: {str(e)}"
        logger.error(
            msg,
            extra={"reader": reader},
            exc_info=True,
        )


#
@router.get("/all_reader")
async def get_all_books(user: Users = Depends(get_current_user)):
    try:
        if user:
            return await ReaderDAO.find_all()
    except SQLAlchemyError as db_err:
        msg = f"Database Exception get all books {db_err}"
        logger.error(msg, exc_info=True, extra={"user": user})
        raise HTTPException(status_code=500, detail=msg)
    except Exception as e:
        msg = f"Unexpected error: {str(e)}"
        logger.error(msg, exc_info=True, extra={"user": user})
        raise HTTPException(status_code=500, detail=msg)


@router.get("/find_one_reader")
async def get_one_reader(
    name: Optional[str] = None,
    email: Optional[str] = None,
    user: Users = Depends(get_current_user),
):
    try:
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
    except SQLAlchemyError as db_err:
        msg = f"Database Exception get one reader {db_err}"
        logger.error(msg, exc_info=True, extra={"user": user})
        raise HTTPException(status_code=500, detail=msg)
    except Exception as e:
        msg = f"Unexpected error: {str(e)}"
        logger.error(msg, exc_info=True, extra={"user": user})
        raise HTTPException(status_code=500, detail=msg)


@router.put("/update_readers")
async def update_reader_data(
    reader_new: SNewReader,
    reader: SReaders = Depends(get_one_reader),
    current_user: Users = Depends(get_current_user),
):
    try:
        if reader:
            new_data = await ReaderDAO.update_data(
                reader.id, name=reader_new.name, email=reader_new.email
            )
            if not new_data:
                raise CannotUpdateDataToDatabase
            raise UpdateDataToDatabase

        else:
            raise MultipleDataToDatabase
    except SQLAlchemyError as db_err:
        msg = f"Database Exception update reader {db_err}"
        logger.error(msg, exc_info=True, extra={"user": current_user})
        raise HTTPException(status_code=500, detail=msg)
    except Exception as e:
        msg = f"Unexpected error: {str(e)}"
        logger.error(msg, exc_info=True, extra={"user": current_user})
        raise HTTPException(status_code=500, detail=msg)


@router.delete("/delete")
async def delete_reader(
    current_user: Users = Depends(get_current_user), reader: SNewReader = Depends()
):
    try:
        if reader:
            await ReaderDAO.delete(name=reader.name, email=reader.email)
            raise ReadersDeleteToDatabase
    except SQLAlchemyError as db_err:
        msg = f"Database Exception delete reader {db_err}"
        logger.error(msg, exc_info=True, extra={"user": current_user})
        raise HTTPException(status_code=500, detail=msg)
    except Exception as e:
        msg = f"Unexpected error: {str(e)}"
        logger.error(msg, exc_info=True, extra={"user": current_user})
        raise HTTPException(status_code=500, detail=msg)
