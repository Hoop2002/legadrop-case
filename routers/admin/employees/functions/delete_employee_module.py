from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from database import get_session
from models import Administrator


async def delete_employee(admin_id: str) -> bool:
    async with get_session() as session:
        try:
            result = await session.execute(
                select(Administrator).filter_by(admin_id=admin_id)
            )
            admin = result.scalar_one_or_none()
            if not admin:
                return False
            await session.delete(admin)
            await session.commit()
            return True
        except NoResultFound:
            return False
