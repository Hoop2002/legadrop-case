from sqlalchemy import select
from sqlalchemy.orm import joinedload
from typing import Sequence
from database import get_session
from models import UserItems


async def get_items_by_user(user_id: str) -> Sequence[UserItems]:
    async with get_session() as session:
        stmt = (
            select(UserItems)
            .options(joinedload(UserItems.item))
            .where(UserItems.user.has(user_id=user_id))
        )
        result = await session.execute(stmt)
        items = result.scalars().all()
        return items
