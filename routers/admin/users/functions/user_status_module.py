from sqlalchemy import update
from database import get_session
from models import User


async def update_user(user_id: str, updated_data: dict):
    """Обновление данных пользователя по user_id."""
    async with get_session() as session:
        await session.execute(
            update(User).where(User.user_id == user_id).values(**updated_data)
        )
        await session.commit()


async def verify_user(user_id: str):
    """Подтверждение пользователя."""
    await update_user(user_id, {"verified": True})


async def activate_user(user_id: str):
    """Активация пользователя."""
    await update_user(user_id, {"active": True})


async def deactivate_user(user_id: str):
    """Деактивация пользователя."""
    await update_user(user_id, {"active": False})
