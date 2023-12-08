from sqlalchemy.future import select
from database import get_session
from models import AdminData, Administrator


async def get_employee(admin_id: str):
    async with get_session() as session:
        result = await session.execute(
            select(Administrator).filter_by(admin_id=admin_id)
        )
        user = result.scalar_one_or_none()
    return user


async def get_by_email(email: str) -> AdminData:
    async with get_session() as session:
        result = await session.execute(select(Administrator).filter_by(email=email))
        user = result.scalar_one_or_none()
    return user


async def get_by_username(username: str):
    async with get_session() as session:
        result = await session.execute(
            select(Administrator).filter_by(username=username)
        )
        user = result.scalar_one_or_none()
    return user
