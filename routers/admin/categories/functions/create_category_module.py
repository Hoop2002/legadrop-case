from database import get_session
from models import Category


async def create_category(name: str) -> Category:
    async with get_session() as session:
        category = Category(name=name)
        session.add(category)
        await session.commit()
        await session.refresh(category)
        return category
