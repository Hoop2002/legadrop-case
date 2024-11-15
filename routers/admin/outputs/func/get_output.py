from sqlalchemy import select
from database import get_session
from models.models import ItemsFindings, Item, User


async def get_outputs(page_size, page):
    async with get_session() as session:
        if page_size and page:
            stmt = select(ItemsFindings).limit(page_size).offset(page * page_size)
        else:
            stmt = select(ItemsFindings)

        itemf_ = await session.execute(stmt)
        outputs = itemf_.scalars().all()

        result = []

        for output in outputs:
            stmt_item = await session.execute(
                select(Item).filter_by(item_id=output.item_id)
            )
            stmt_user = await session.execute(
                select(User).filter_by(user_id=output.user_id)
            )

            item_ = stmt_item.scalar_one_or_none()
            user_ = stmt_user.scalar_one_or_none()

            result.append(
                {
                    "genshin_user_id": output.genshin_user_id,
                    "itemfs_id": output.itemfs_id,
                    "user_id": output.user_id,
                    "username": user_.username if user_.username else user_.email,
                    "active": output.active,
                    "total": output.total,
                    "id": output.id,
                    "item_name": item_.name,
                    "item_id": output.item_id,
                    "status": output.status,
                }
            )

        return result


async def get_output(itemfs_id):
    async with get_session() as session:
        stmt = await session.execute(
            select(ItemsFindings).filter_by(itemfs_id=itemfs_id)
        )
        output = stmt.scalar_one_or_none()

        return output
