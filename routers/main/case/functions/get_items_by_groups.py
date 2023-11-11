from models import RarityCategory
from sqlalchemy.future import select
from database import get_session
import random


async def get_items_by_groups(items: dict):
    async with get_session() as session:
        COMMON = await session.execute(
            select(RarityCategory).filter_by(ext_id="COMMON")
        )
        UNCOMMON = await session.execute(
            select(RarityCategory).filter_by(ext_id="UNCOMMON")
        )
        RARE = await session.execute(select(RarityCategory).filter_by(ext_id="RARE"))
        MYTHICAL = await session.execute(
            select(RarityCategory).filter_by(ext_id="MYTHICAL")
        )
        LEGENDARY = await session.execute(
            select(RarityCategory).filter_by(ext_id="LEGENDARY")
        )
        ULTRALEGENDARY = await session.execute(
            select(RarityCategory).filter_by(ext_id="ULTRALEGENDARY")
        )

        COMMON = COMMON.scalar_one_or_none()
        UNCOMMON = UNCOMMON.scalar_one_or_none()
        RARE = RARE.scalar_one_or_none()
        MYTHICAL = MYTHICAL.scalar_one_or_none()
        LEGENDARY = LEGENDARY.scalar_one_or_none()
        ULTRALEGENDARY = ULTRALEGENDARY.scalar_one_or_none()

        GROUP = random.choices(
            [COMMON, UNCOMMON, RARE, MYTHICAL, LEGENDARY, ULTRALEGENDARY],
            weights=[
                float(COMMON.category_percent),
                float(UNCOMMON.category_percent),
                float(RARE.category_percent),
                float(MYTHICAL.category_percent),
                float(LEGENDARY.category_percent),
                float(ULTRALEGENDARY.category_percent),
            ],
        )[-1]

        
