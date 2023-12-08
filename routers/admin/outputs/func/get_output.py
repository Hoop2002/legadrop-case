from sqlalchemy import select
from database import get_session
from models.models import ItemsFindings


async def get_outputs():
    async with get_session() as session:
        stmt = await session.execute(select(ItemsFindings))
        outputs = stmt.scalars().all()

        return outputs


async def get_output(itemfs_id):
    async with get_session() as session:
        stmt = await session.execute(
            select(ItemsFindings).filter_by(itemfs_id=itemfs_id)
        )
        output = stmt.scalar_one_or_none()

        return output
