from sqlalchemy.future import select
from database import get_session
from models import Permission

async def get_permissions():
    async with get_session() as session:
        permissions_data = await session.execute(select(Permission))
        permissions = permissions_data.scalars().all()
        return permissions

#exaplme of using this function
# all_permissions = await get_permissions()
# for permission in all_permissions:
#     print(permission.name)
