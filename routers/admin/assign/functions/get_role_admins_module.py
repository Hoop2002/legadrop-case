from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from database import get_session
from models import Role


async def get_role_admins(role_name: str):
    async with get_session() as session:
        # Получаем роль из базы данных вместе со связанными администраторами
        result_role = await session.execute(
            select(Role).options(joinedload(Role.administrators)).where(Role.name == role_name)
        )
        role = result_role.scalars().first()

        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Роль '{role_name}' не найдена!")

        # Возвращаем список администраторов, которым назначена данная роль
        admins = role.administrators
        return admins
