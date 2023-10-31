from sqlalchemy import select
from typing import Optional
from database import get_session
from models import Item

async def update_item(item_id: str, name: str, image: str) -> Optional[Item]:
    async with get_session() as session:
        result = await session.execute(select(Item).filter_by(item_id=item_id))
        item = result.scalars().first()
        item.name = name  # type: ignore
        item.image = image  # type: ignore
        await session.commit()
        await session.refresh(item)
        return item

