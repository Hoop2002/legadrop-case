from sqlalchemy import update

from database import get_session
from models.models import ItemsFindings



async def change_status_output(itemfs_id: str, status: str):
    async with get_session() as session:
        stmt = update(ItemsFindings).where(ItemsFindings.itemfs_id == itemfs_id).values({"status": status})
        await session.execute(stmt)
        await session.commit()
