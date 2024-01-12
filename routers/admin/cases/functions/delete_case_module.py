from sqlalchemy import select
from database import get_session
from models import Case


async def delete_case(case_id: str) -> bool:
    async with get_session() as session:
        result = await session.execute(select(Case).filter_by(case_id=case_id))
        case = result.scalars().first()
        if case is None:
            return False
        await session.delete(case)
        await session.commit()
        return True
