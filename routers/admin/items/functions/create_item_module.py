from database import get_session
from models import Item

async def create_item(item) -> Item:
    async with get_session() as session:
        session.add(item)
        await session.commit()
        await session.refresh(item)
        return item

