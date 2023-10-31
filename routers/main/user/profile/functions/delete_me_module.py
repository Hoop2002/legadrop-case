from sqlalchemy.future import select
from database import get_session
from models import User


async def _get_me_by_filter(**kwargs):
    """Приватная функция помощник для получения пользователя по заданному фильтру."""
    async with get_session() as session:
        data = await session.execute(select(User).filter_by(**kwargs))
        return data.scalar_one_or_none()


async def get_me(user_id: str):
    """Получение пользователя по user_id."""
    return await _get_me_by_filter(user_id=user_id)


async def delete_me(user_id: str):
    """Удаление пользователя по user_id."""
    async with get_session() as session:
        user = await _get_me_by_filter(user_id=user_id)
        if user:
            await session.delete(user)
            await session.commit()
