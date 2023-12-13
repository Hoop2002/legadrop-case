from models.models import OrderMoogold
from database import get_session
from sqlalchemy import select

async def get_orders_list(itemfs_id: str):
    async with get_session() as session:
        stmt = select(OrderMoogold).where(OrderMoogold.itemfs_id == itemfs_id)
        result = await session.execute(stmt)
        objects_ = result.scalars().all()

        return objects_
