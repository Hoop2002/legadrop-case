from sqlalchemy import update
from database import get_session
from security.password_functions import hash_password
from models import User


async def update_me(user_id: str, updated_data: dict):
    """Обновление данных пользователя по user_id."""
    async with get_session() as session:
        await session.execute(
            update(User).where(User.user_id == user_id).values(**updated_data)
        )
        await session.commit()

async def update_password(user_id: str, password: str):
    """Обновление пароля пользователя."""
    hashed_password = await hash_password(password)
    await update_me(user_id, {"password_hash": hashed_password})
