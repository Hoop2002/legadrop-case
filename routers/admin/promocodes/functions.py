from sqlalchemy import select
from typing import Sequence
from database import get_session
from models import PromoCode, User


async def used_promo(code_data, user_id):
    async with get_session() as session:
        stmt = (
            select(PromoCode.id)
            .filter_by(code_data=code_data, active=True).filter(PromoCode.users.any(User.user_id == user_id))
        )
        result = await session.execute(stmt)
        result = result.scalar()
        if result:
            return True
        return False


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
