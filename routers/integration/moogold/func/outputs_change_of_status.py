from sqlalchemy import update

from database import get_session
from models.models import ItemsFindings


async def change_status_output_moogold(itemfs_id: str):
    async with get_session() as session:
        stmt = (
            update(ItemsFindings)
            .where(ItemsFindings.itemfs_id == itemfs_id)
            .values({"status": "MOOGOLD"})
            .returning(ItemsFindings)
        )
        await session.execute(stmt)
        await session.commit()
