from sqlalchemy import select
from typing import Optional
from database import get_session
from models import Category


async def get_category(category_id: str) -> Optional[Category]:
    async with get_session() as session:
        result = await session.execute(
            select(Category).filter_by(category_id=category_id)
        )
        return result.scalars().first()


async def get_category_by_name(name: str) -> Optional[Category]:
    async with get_session() as session:
        result = await session.execute(select(Category).filter_by(name=name))
        return result.scalars().first()
