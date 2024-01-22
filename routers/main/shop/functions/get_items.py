from sqlalchemy import select
from sqlalchemy.orm import joinedload
from typing import Sequence, Optional
from database import get_session
from models import Item


async def get_items() -> Sequence[Item]:
    async with get_session() as session:
        stmt = (
            select(Item)
            .options(joinedload(Item.rarity_category))
        )
        result = await session.execute(stmt)
        items = result.scalars().all()
        return items


async def get_item_by_id(item_id: int) -> Optional[Item]:
    async with get_session() as session:
        stmt = (
            select(Item).filter_by(id=item_id)
        )
        result = await session.execute(stmt)
        items = result.scalars().first()
        return items
