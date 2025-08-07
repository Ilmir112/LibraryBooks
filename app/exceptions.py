from fastapi import HTTPException, status


class BooksException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BooksException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class IncorrectEmailOrPasswordException(BooksException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"


class TokenExpiredException(BooksException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Срок действия токена истек"


class TokenAbsentException(BooksException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectTokenFormatException(BooksException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class FindNotBooksException(BooksException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Книга не найдена"


class BooksCancelException(BooksException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Нет доступных экземпляров книги"


class FindBorrowedBookAndReaderException(BooksException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Данный экземпляр уже выдан читателю"


class FindReaderException(BooksException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Читатель не найден"


class FindBookAndReaderException(BooksException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Читатель уже взял 3 книги"


class UserIsNotPresentException(BooksException):
    status_code = status.HTTP_401_UNAUTHORIZED


class RoomFullyBooked(BooksException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Не осталось свободных номеров"


class BooksCannotBeBooked(BooksException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось добавить ввиду неизвестной ошибки"


class ReadersNotBorrowedBookException(BooksException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "У читателя нет не сданных книг"


class BooksCannotNullBeBooked(BooksException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Не удалось принять книгу так как книга не получена данным пользователем"


class CannotAddDataToDatabase(BooksException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось добавить запись"


class CannotUpdateDataToDatabase(BooksException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось обновить запись"


class UpdateNotDataToDatabase(BooksException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пароль и логин совпадают с предыдущим"


class UpdateDataToDatabase(BooksException):
    status_code = status.HTTP_200_OK
    detail = "Данные обновлены"


class MultipleDataToDatabase(BooksException):
    status_code = status.HTTP_200_OK
    detail = "Найдено несколько читателей, должен быть только один"


class BooksDeleteToDatabase(BooksException):
    status_code = status.HTTP_200_OK
    detail = "Книга удалена"


class ReadersDeleteToDatabase(BooksException):
    status_code = status.HTTP_200_OK
    detail = "Читатель удален"
