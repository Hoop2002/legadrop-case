from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from database import get_session
from models import Role, Administrator


async def assign_role(username: str, role_name: str):
    async with get_session() as session:
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

        # Получаем роль по имени из базы данных
        result_role = await session.execute(select(Role).where(Role.name == role_name))
        role = result_role.scalars().first()

        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Роль '{role_name}' не найдена!",
            )

        if role not in admin.roles:
            admin.roles.append(role)

        await session.commit()

        return admin, role
