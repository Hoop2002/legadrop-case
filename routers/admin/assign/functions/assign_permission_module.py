from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from database import get_session
from models import Role, Permission



async def assign_permission(role_name: str, permissions_names: list):
    async with get_session() as session:
        result_role = await session.execute(
            select(Role).options(joinedload(Role.permissions)).where(Role.name == role_name)
        )
        role = result_role.scalars().first()
        
        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Роль '{role_name}' не найдена!")
        
        # Удаляем все разрешения у роли
        role.permissions = []
        
        # Получаем все разрешения из списка permission_names из базы данных
        result_permissions = await session.execute(
            select(Permission).where(Permission.name.in_(permissions_names))
        )
        permissions = result_permissions.scalars().all()
        
        for permission in permissions:
            # Так как мы уже удалили все разрешения у роли, просто добавляем новые
            role.permissions.append(permission)
        
        await session.commit()
        
        return role, permissions


# async def assign_permission(role_name: str, permissions_names: list):
#     async with get_session() as session:
#         result_role = await session.execute(
#             select(Role).options(joinedload(Role.permissions)).where(Role.name == role_name)
#         )
#         role = result_role.scalars().first()
        
#         if not role:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Роль '{role_name}' не найдена!")
        
#         # Получаем все разрешения из списка permission_names из базы данных
#         result_permissions = await session.execute(
#             select(Permission).where(Permission.name.in_(permissions_names))
#         )
#         permissions = result_permissions.scalars().all()
        
#         for permission in permissions:
#             # Если разрешение еще не связано с ролью, добавляем его
#             if permission not in role.permissions:
#                 role.permissions.append(permission)
        
#         await session.commit()
        
#         return role, permissions
