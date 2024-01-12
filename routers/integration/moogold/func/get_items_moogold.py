from sqlalchemy import select
from typing import Optional
from database import get_session
from models.models import Item, ItemCompound
from routers.integration import moogold


async def get_items_key_moogold(item):
    async with get_session() as session:
        moogold_ids = []
        stmt = select(ItemCompound).where(ItemCompound.item_id == item)
        result = await session.execute(stmt)
        objects = result.scalars().all()

        for key in objects:
            items_moogold = [key.moogold_id] * key.quantity

            moogold_ids.append(i for i in items_moogold)

        return moogold_ids
