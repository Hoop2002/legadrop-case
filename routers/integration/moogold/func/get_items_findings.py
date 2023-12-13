from sqlalchemy import select
from typing import Optional
from database import get_session
from models.models import ItemsFindings
from routers.integration import moogold


async def get_itemfs(itemfs_id: str):
    async with get_session() as session:
        stmt = select(ItemsFindings).where(ItemsFindings.itemfs_id == itemfs_id)
        result = await session.execute(stmt)
        object_ = result.scalars().one_or_none()

        return object_
    