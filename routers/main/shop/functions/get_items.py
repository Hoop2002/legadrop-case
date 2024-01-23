from sqlalchemy import select
from sqlalchemy.orm import joinedload
from typing import Sequence, Optional
from database import get_session
from models import Item


async def get_items(
    filter_by: dict = None, page_size: int = 20, page: int = 0
) -> Sequence[Item]:
    async with get_session() as session:
        stmt = (
            select(Item)
            .filter_by(**filter_by)
            .options(joinedload(Item.rarity_category))
            .limit(page_size)
            .offset(page * page_size)
        )
        result = await session.execute(stmt)
        items = result.scalars().all()
        return items


async def get_item_by_id(item_id: int) -> Optional[Item]:
    async with get_session() as session:
        stmt = select(Item).filter_by(id=item_id)
        result = await session.execute(stmt)
        items = result.scalars().first()
        return items
