from sqlalchemy.future import select
from database import get_session
from models import User


async def _get_user_by_filter(**kwargs):
    """Приватная функция помощник для получения пользователя по заданному фильтру."""
    async with get_session() as session:
        data = await session.execute(select(User).filter_by(**kwargs))
        return data.scalar_one_or_none()


async def get_user_by_username(username: str):
    """Получение пользователя по имени пользователя."""
    return await _get_user_by_filter(username=username)


async def get_user_by_email(email: str):
    """Получение пользователя по электронной почте."""
    return await _get_user_by_filter(email=email)


async def is_username_taken(username: str) -> bool:
    """Проверка, занято ли имя пользователя."""
    return await get_user_by_username(username) is not None


async def is_email_taken(email: str) -> bool:
    """Проверка, занят ли адрес электронной почты."""
    return await get_user_by_email(email) is not None
