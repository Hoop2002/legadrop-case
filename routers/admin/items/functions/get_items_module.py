from sqlalchemy import select
from sqlalchemy.orm import joinedload
from typing import Sequence
from database import get_session
from models import Item
from models.models import ItemCompound


async def get_items() -> Sequence[Item]:
    async with get_session() as session:
        result = await session.execute(select(Item).options(joinedload(Item.compound)))
        items = result.scalars().unique().all()

        return items
