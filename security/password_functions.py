from fastapi import status, HTTPException
import os
import logging
import secrets
import string
from dotenv import load_dotenv
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHashError, VerificationError

# Настройка логирования
logging.basicConfig(level=logging.INFO)
hasher = PasswordHasher()
load_dotenv()
VERIFY_SECRET = str(os.getenv("VERIFY_SECRET"))


async def password_generator(length=8, uppercase=True, digits=True, characters=False):
    alphabet = string.ascii_lowercase
    if uppercase:
        alphabet += string.ascii_uppercase
    if digits:
        alphabet += string.digits
    if characters:
        alphabet += string.punctuation

    password = "".join(secrets.choice(alphabet) for _ in range(length))

    return password


async def hash_password(password: str) -> str:
    password = password + VERIFY_SECRET
    return hasher.hash(password)


async def verify_password(hashed_password: str, password: str) -> bool:
    password_with_secret = password + VERIFY_SECRET
    try:
        hasher.verify(hash=hashed_password, password=password_with_secret)
        return True
    except VerifyMismatchError:
        logging.warning("Пароль не совпадает с хэшем.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный пароль."
        )
    except InvalidHashError:
        logging.error("Пароль был неправильно сохранён в базе.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера.",
        )
    except VerificationError as ve:
        logging.error(f"Ошибка проверки пароля: {ve}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера.",
        )
