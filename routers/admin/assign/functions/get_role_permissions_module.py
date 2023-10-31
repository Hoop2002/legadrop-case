from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from database import get_session
from models import Role

from typing import List
async def get_role_permissions(role_name: str):
    async with get_session() as session:
        # Получаем роль из базы данных вместе с ее разрешениями
        result_role = await session.execute(
            select(Role).options(joinedload(Role.permissions)).where(Role.name == role_name)
        )
        role = result_role.scalars().first()

        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Роль '{role_name}' не найдена!")

        permissions = role.permissions
        return permissions



