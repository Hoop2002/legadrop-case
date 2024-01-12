from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from database import get_session
from models import Case


async def get_cases():
    async with get_session() as session:
        result = await session.execute(select(Case).options(joinedload(Case.category)))
        return result.scalars().all()
