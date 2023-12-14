from sqlalchemy import insert, select
from database import get_session
from models.models import ItemsFindings, ItemsFindingsStatus, User, Item


async def create_output_(outputs):
    async with get_session() as session:
        items_output = outputs.pop("outputs")
        genshin_id = outputs.get("genshin_user_id")

        user = await session.execute(
            select(User).filter_by(user_id=outputs.get("user_id"))
        )
        status = await session.execute(
            select(ItemsFindingsStatus).filter_by(ext_id="EXPECT")
        )

        user_ = user.scalar_one_or_none().user_id
        status_ = status.scalar_one_or_none().ext_id

        for itemf in items_output:
            itemf["user_id"] = user_
            itemf["genshin_user_id"] = genshin_id
            itemf["status"] = status_

            total = await session.execute(
                select(Item).filter_by(item_id=itemf.get("item_id"))
            )

            total_ = total.scalar_one_or_none().cost

            itemf["total"] = total_

        stmt = insert(ItemsFindings).values(items_output).returning(ItemsFindings)

        output = await session.execute(stmt)
        await session.commit()
        output_ = output.scalars().all()

        for i in output_:
            await session.refresh(i)

        return output_
