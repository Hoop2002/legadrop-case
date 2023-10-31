from sqlalchemy import update
from database import get_session
from models import User


async def update_me(user_id: str, updated_data: dict):
    """Обновление данных пользователя по user_id."""
    async with get_session() as session:
        await session.execute(
            update(User).where(User.user_id == user_id).values(**updated_data)
        )
        await session.commit()


async def update_me_image(user_id: str, path: str):
    """Обновление аватара пользователя."""
    await update_me(user_id, {"image": path})


async def update_me_username(user_id: str, username: str):
    """Обновление имени пользователя."""
    await update_me(user_id, {"username": username})


async def update_me_email(user_id: str, email: str):
    """Обновление электронной почты пользователя."""
    await update_me(user_id, {"email": email})


async def update_me_locale(user_id: str, locale: str):
    """Обновление локали пользователя."""
    await update_me(user_id, {"locale": locale})
