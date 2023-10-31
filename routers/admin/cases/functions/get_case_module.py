from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from typing import Optional
from database import get_session
from models import Case

async def get_case(case_id: str):
    async with get_session() as session:
        result = await session.execute(
            select(Case).options(joinedload(Case.category)).filter_by(case_id=case_id)
        )
        return result.scalars().first()

async def get_case_by_name(name: str) -> Optional[Case]:
    async with get_session() as session:
        result = await session.execute(select(Case).filter_by(name=name))
        return result.scalars().first()
