from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from database import get_session
from models import Permission


async def get_permission_roles(permission_name: str):
    async with get_session() as session:
        # Получаем разрешение из базы данных вместе со связанными ролями
        result_permission = await session.execute(
            select(Permission).options(joinedload(Permission.roles)).where(Permission.name == permission_name)
        )
        permission = result_permission.scalars().first()

        if not permission:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Разрешение '{permission_name}' не найдено!")

        # Возвращаем список ролей, связанных с этим разрешением
        roles = permission.roles
        return roles