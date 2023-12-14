from sqlalchemy import delete, update
from database import get_session
from models.models import ItemsFindings


async def delete_output_(itemfs_id):
    async with get_session() as session:
        stmt = (
            delete(ItemsFindings)
            .where(ItemsFindings.itemfs_id == itemfs_id)
            .returning(ItemsFindings)
        )

        del_out = await session.execute(stmt)
        await session.commit()
        delete_output_obj = del_out.scalar_one_or_none()
        # await session.refresh(delete_output_obj)
        return delete_output_obj


async def inactive_output(itemsf_id):
    async with get_session() as session:
        stmt = (
            update(ItemsFindings)
            .where(ItemsFindings.itemfs_id == itemsf_id)
            .values({"active": False, "status": "CANCELLED"})
            .returning(ItemsFindings)
        )

        inactive_outputs = await session.execute(stmt)
        await session.commit()
        out = inactive_outputs.scalar_one_or_none()
        return out
