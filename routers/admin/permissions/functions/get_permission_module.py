from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from database import get_session
from models import Permission

async def get_permission(permission_id: str) -> Permission:
    async with get_session() as session:
        permission_data = await session.execute(select(Permission).where(Permission.permission_id == permission_id))
        permission = permission_data.scalar_one_or_none()
        return permission
    
async def get_permission_by_name(permission_name: str) -> Permission:
    async with get_session() as session:
        permission_data = await session.execute( select( Permission ).where( Permission.name == permission_name ) )
        permission = permission_data.scalar_one_or_none()  
        return permission

async def get_permission_name(permission_id: str):
    permission = await get_permission(permission_id)
    return permission.name


async def get_permission_id(permission_name: str):
    permission = await get_permission_by_name(permission_name)
    return permission.permission_id