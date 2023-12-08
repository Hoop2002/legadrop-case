from database import get_session
from models import Permission


async def create_permission(permission: str) -> Permission:
    async with get_session() as session:
        permission = Permission(name=permission)
        session.add(permission)
        await session.flush()
        return permission
