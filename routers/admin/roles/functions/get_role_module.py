from fastapi import HTTPException, status
from sqlalchemy.future import select
from database import get_session
from models import Role, ResponseRole

async def get_role(role_id: str) -> ResponseRole:
    async with get_session() as session:
        role_data = await session.execute(select(Role).where(Role.role_id == role_id))
        role = role_data.scalar_one_or_none()
        if role is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Роль с ID {role_id} не найдена.",
            )
        return role

async def get_role_by_name(role_name: str) -> ResponseRole:
    async with get_session() as session:
        role_data = await session.execute(select(Role).where(Role.name == role_name))
        role = role_data.scalar_one_or_none()
        return role
