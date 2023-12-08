from sqlalchemy.future import select
from database import get_session
from models import Role


async def get_roles():
    async with get_session() as session:
        roles_data = await session.execute(select(Role))
        roles = roles_data.scalars().all()
        return roles


# example of using this function
# all_roles = await get_roles()
# for role in all_roles:
#     print(role.name)
