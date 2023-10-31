from sqlalchemy import select
from typing import Sequence, Optional
from database import get_session
from models import Item

async def create_item(name: str, image: str) -> Item:
    async with get_session() as session:
        item = Item(name=name, image=image)
        session.add(item)
        await session.commit()
        await session.refresh(item)
        return item

async def get_items() -> Sequence[Item]:
    async with get_session() as session:
        result = await session.execute(select(Item))
        return result.scalars().all()

async def get_item(item_id: str) -> Optional[Item]:
    async with get_session() as session:
        result = await session.execute(select(Item).filter_by(item_id=item_id))
        return result.scalars().first()

async def get_item_by_name(name: str) -> Optional[Item]:
    async with get_session() as session:
        result = await session.execute(select(Item).filter_by(name=name))
        return result.scalars().first()

async def update_item(item_id: str, name: str, image: str) -> Optional[Item]:
    async with get_session() as session:
        result = await session.execute(select(Item).filter_by(item_id=item_id))
        item = result.scalars().first()
        item.name = name  # type: ignore
        item.image = image  # type: ignore
        await session.commit()
        await session.refresh(item)
        return item

async def delete_item(item_id: str) -> bool:
    async with get_session() as session:
        result = await session.execute(select(Item).filter_by(item_id=item_id))
        item = result.scalars().first()
        if item is None:
            return False
        await session.delete(item)
        await session.commit()
        return True