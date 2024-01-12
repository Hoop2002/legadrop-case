from sqlalchemy import select, update
from typing import Optional
from database import get_session
from models import Item


async def update_item(data: dict):
    async with get_session() as session:
        stmt = (
            update(Item)
            .where(Item.item_id == data.get("item_id"))
            .values(**data)
            .returning(Item)
        )
        result = await session.execute(stmt)
        await session.commit()
        item = result.scalar_one_or_none()
        await session.refresh(item)
        return item
