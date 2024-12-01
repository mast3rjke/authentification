from typing import Tuple, Dict
from json import dumps, loads

# Доступные значения для операций
ALLOWED_OPERATION_ID: Tuple[int, int] = (1, 2)
# Название файла для хранения логинов и паролей
LOGIN_PASSWORD_FILE_NAME: str = "auth_file.txt"\
# Кодировка файла
FILE_ENCODING: str = "utf-8"


def read_login_password_file() -> Dict[str, str]:
    """
    Получение данных о логинах и паролях

    :return: словарь вида логин:пароль
    """
    try:
        with open(LOGIN_PASSWORD_FILE_NAME, "r", encoding=FILE_ENCODING) as file:
            return loads(file.read() or "{}")
    except FileNotFoundError:
        with open(LOGIN_PASSWORD_FILE_NAME, "w+", encoding=FILE_ENCODING):
            return read_login_password_file()


# Словарь для хранения логинов и паролей
LOGIN_PASSWORD_DICT: Dict[str, str] = read_login_password_file()


def register(login_in: str, password: str) -> bool:
    """
    Регистрация пользователя с проверкой существования логина

    :param login_in: логин
    :param password: пароль
    :return: успешность операции
    """
    if login_in in LOGIN_PASSWORD_DICT:
        raise RuntimeError("Логин уже существует!")

    LOGIN_PASSWORD_DICT[login_in] = password

    return True


def login(login_in: str, password: str) -> bool:
    """
    Аутентификация пользователя

    :param login_in: логин
    :param password: пароль
    :return: успешность операции
    """
    if login_in not in LOGIN_PASSWORD_DICT:
        raise RuntimeError("Логин не найден!")

    if password != LOGIN_PASSWORD_DICT[login_in]:
        raise RuntimeError("Неверный пароль")

    return True


def get_operation_id() -> int:
    """
    Получение идентификатора действия

    :return: идентификатор действия
    """
    try:
        operation_id: int = int(
            input("Введите 1 - для авторизации, 2 - для регистрации: ")
        )
    except ValueError:
        print("Возможно, Вы ввели не число!")
        return get_operation_id()
    else:
        if operation_id not in ALLOWED_OPERATION_ID:
            print("Нет такой операции!")
            return get_operation_id()

        return operation_id


def get_login_and_password() -> Tuple[str, str]:
    """
    Получение логина и пароля с проверкой на непустоту

    :return: логин и пароль
    """
    login_in: str = input("Введите логин: ")
    password: str = input("Введите пароль: ")

    if not login_in or not password:
        print("Значение не может быть пустым!")
        return get_login_and_password()

    return login_in, password


def process() -> None:
    """Основной процесс приложения"""
    operation_id: int = get_operation_id()
    login_in, password = get_login_and_password()

    try:
        if operation_id == 1:
            login(login_in, password)
        else:
            register(login_in, password)
    except RuntimeError as ex:
        print(f"Ошибка: {ex}")

    # В конце работы сохраним все логины и пароли в файл
    with open(LOGIN_PASSWORD_FILE_NAME, "w+", encoding=FILE_ENCODING) as file:
        file.write(dumps(LOGIN_PASSWORD_DICT))


if __name__ == "__main__":
    process()
