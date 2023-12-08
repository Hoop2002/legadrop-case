from sqlalchemy.future import select
from database import get_session
from models import Category


async def delete_category(category_id: str) -> bool:
    async with get_session() as session:
        result = await session.execute(
            select(Category).filter_by(category_id=category_id)
        )
        category = result.scalars().first()
        await session.delete(category)
        await session.commit()
        return True
