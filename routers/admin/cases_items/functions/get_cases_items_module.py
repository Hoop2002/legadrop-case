from enum import unique
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from typing import Sequence
from database import get_session
from models import Case


async def get_cases_items() -> Sequence[Case]:
    async with get_session() as session:
        result = await session.execute(select(Case).options(joinedload(Case.items)))
        return result.scalars().unique().all()
