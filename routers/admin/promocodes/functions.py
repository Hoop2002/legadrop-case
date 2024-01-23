from sqlalchemy import select
from sqlalchemy.orm import joinedload
from typing import Sequence, Optional
from database import get_session
from models import PromoCode


async def get_promo(
    filter_by: dict = {}, page_size: int = 20, page: int = 0
) -> Sequence[PromoCode]:
    async with get_session() as session:
        stmt = (
            select(PromoCode)
            .filter_by(**filter_by)
            .limit(page_size)
            .offset(page * page_size)
        )
        result = await session.execute(stmt)
        promo = result.scalars().all()
        return promo
