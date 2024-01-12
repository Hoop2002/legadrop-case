from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from database import get_session
from models import Administrator


async def get_admin_role(username: str):
    async with get_session() as session:
        # Получаем администратора из базы данных вместе со связанными ролями
        result_admin = await session.execute(
            select(Administrator)
            .options(joinedload(Administrator.roles))
            .where(Administrator.username == username)
        )
        admin = result_admin.scalars().first()

        if not admin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Администратор '{username}' не найден!",
            )

        # Возвращаем список ролей, связанных с этим администратором
        roles = admin.roles
        return roles
