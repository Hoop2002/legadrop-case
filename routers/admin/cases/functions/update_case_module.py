from sqlalchemy import select, update
from typing import Optional
from database import get_session
from models import Case


async def _update_case(data: dict):
    async with get_session() as session:
        stmt = (
            update(Case).
            where(Case.case_id == data.get("case_id")).
            values(**data).
            returning(Case)
        )

        result = await session.execute(stmt)
        await session.commit()
        case = result.scalar_one_or_none()
        await session.refresh(case)
        return case


