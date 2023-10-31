from sqlalchemy import select
from sqlalchemy.orm import joinedload
from typing import Sequence
from database import get_session
from models import Item


async def get_items() -> Sequence[Item]:
    async with get_session() as session:
        result = await session.execute(select(Item).options(joinedload(Item.compound)))
        return result.scalars().unique().all()


