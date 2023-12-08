from sqlalchemy import select
from typing import Optional
from database import get_session
from models import Category


async def update_category(category_id: str, name: str) -> Optional[Category]:
    async with get_session() as session:
        result = await session.execute(
            select(Category).filter_by(category_id=category_id)
        )
        category = result.scalars().first()
        category.name = name  # type: ignore
        await session.commit()
        await session.refresh(category)
        return category
