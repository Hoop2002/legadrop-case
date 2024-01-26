from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from database import get_session
from models import Case


async def get_cases(page: int = 0, page_size: int = 20, filter_by: dict = {}):
    async with get_session() as session:
        stmt = (
            select(Case)
            .filter_by(**filter_by)
            .options(joinedload(Case.category))
            .limit(page_size)
            .offset(page * page_size)
        )
        result = await session.execute(stmt)
        return result.scalars().all()
