from sqlalchemy import select
from sqlalchemy.orm import joinedload
from typing import Optional
from database import get_session
from models import Case


async def get_case_items(case_id: str) -> Optional[Case]:
    async with get_session() as session:
        result = await session.execute(
            select(Case).options(joinedload(Case.items)).filter_by(case_id=case_id)
        )
        return result.scalars().first()
