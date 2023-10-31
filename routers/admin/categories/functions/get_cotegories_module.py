from sqlalchemy import select
from typing import Sequence
from database import get_session
from models import Category

async def get_categories() -> Sequence[Category]:
    async with get_session() as session:
        result = await session.execute(select(Category))
        return result.scalars().all()