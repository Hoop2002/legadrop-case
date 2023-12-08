from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from models import Administrator
from database import get_session


async def get_employees():
    async with get_session() as session:
        result = await session.execute(select(Administrator))
        employees = result.scalars().all()
        return employees


async def get_emoployees_data():
    async with get_session() as session:
        result = await session.execute(
            select(Administrator).options(joinedload(Administrator.roles))
        )
        admins = result.scalars().unique().all()

        admins_with_roles = [
            {"employee": admin, "role": admin.roles} for admin in admins
        ]
        return admins_with_roles
