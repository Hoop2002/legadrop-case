from database import get_session
from models.models import ItemsFindings, OrderMoogold


async def write_order_id_in_itemfs(itemfs_id: str, order_id: str):
    async with get_session() as session:
        order = OrderMoogold(order_id=order_id, itemfs_id=itemfs_id)
        session.add(order)
        await session.commit()
        await session.flush(order)
