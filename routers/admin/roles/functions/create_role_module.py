from database import get_session
from models import Role


async def create_role(role: str) -> Role:
    async with get_session() as session:
        role = Role(name=role)
        session.add(role)
        await session.commit()
        return role
