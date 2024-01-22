from sqlalchemy import select
from sqlalchemy.orm import joinedload
from typing import Sequence
from database import get_session
from models import UserItems, Item


async def get_items_by_user(user_id: str, page_size: int = 20, page: int = 0) -> Sequence[UserItems]:
    async with get_session() as session:
        stmt = (
            select(UserItems)
            .options(joinedload(UserItems.item).subqueryload(Item.rarity_category))
            .where(UserItems.user.has(user_id=user_id)).limit(page_size).offset(page * page_size)
        )
        result = await session.execute(stmt)
        items = result.scalars().all()
        return items
