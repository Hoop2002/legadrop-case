from fastapi import HTTPException, status
from sqlalchemy.future import select
from models import Permission
from database import get_session


async def delete_permission(permission_id: str) -> None:
    async with get_session() as session:
        permission_data = await session.execute(select(Permission).where(Permission.permission_id == permission_id))
        permission =permission_data.scalar_one_or_none()
        if permission is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Разрешение не найдено")
        await session.delete(permission)

async def delete_permission_by_name(permission_name: str) -> None:
    async with get_session() as session:
        permission_data = await session.execute(select(Permission).where(Permission.name == permission_name))
        permission = permission_data.scalar_one_or_none()
        if permission is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Разрешение не найдено")
        await session.delete(permission)
