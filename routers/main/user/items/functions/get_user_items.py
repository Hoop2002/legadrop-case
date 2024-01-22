from sqlalchemy import select
from sqlalchemy.orm import joinedload
from typing import Sequence
from database import get_session
from models import Item, User


async def get_items_by_user(user_id: str) -> Sequence[Item]:
    async with get_session() as session:
        stmt = (
            select(Item)
            .options(joinedload(Item.rarity_category))
            .where(Item.user_items.any(User.user_id == user_id))
        )
        result = await session.execute(stmt)
        items = result.scalars().all()
        return items
