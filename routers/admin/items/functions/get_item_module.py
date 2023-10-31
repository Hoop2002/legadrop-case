from sqlalchemy import select
from typing import Optional
from database import get_session
from models import Item


async def get_item(item_id: str) -> Optional[Item]:
    async with get_session() as session:
        result = await session.execute(select(Item).filter_by(item_id=item_id))
        return result.scalars().first()

async def get_item_by_name(name: str) -> Optional[Item]:
    async with get_session() as session:
        result = await session.execute(select(Item).filter_by(name=name))
        return result.scalars().first()

