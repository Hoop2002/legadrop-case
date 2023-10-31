from fastapi import HTTPException, status
from sqlalchemy.future import select
from models import Role
from database import get_session


async def delete_role(role_id: str) -> None:
    async with get_session() as session:
        role_data = await session.execute(select(Role).where(Role.role_id == role_id))
        role = role_data.scalar_one_or_none()
        if role is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Роль не найдена")
        await session.delete(role)


async def delete_role_by_name(role_name: str) -> None:
    async with get_session() as session:
        role_data = await session.execute(select(Role).where(Role.name == role_name))
        role = role_data.scalar_one_or_none()
        if role is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Роль не найдена")
        await session.delete(role)
