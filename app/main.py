import time

import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from app.books.router import router as router_books
from app.borrowed_book.router import router as router_borrowed_book
from app.logger import logger
from app.reader.router import router as router_reader
from app.users.router import router_auth, router_users

app = FastAPI(
    title="Библиотека",
    version="0.1.0",
    root_path="/api",
)


# Обработка ошибок валидации
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"validation_exception: {exc.errors()}, body: {exc.body}")
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "body": exc.body,
            "message": "validation exception",
        },
    )


app.include_router(router_auth)
app.include_router(router_users)
app.include_router(router_books)
app.include_router(router_reader)
app.include_router(router_borrowed_book)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    # При подключении Prometheus + Grafana подобный лог не требуется
    logger.info("Request handling time", extra={"process_time": round(process_time, 4)})
    return response


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
