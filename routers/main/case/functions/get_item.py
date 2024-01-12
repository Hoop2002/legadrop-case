from difflib import restore
from token import RARROW
from sqlalchemy.future import select
from database import get_session
from models import User, Item, RarityCategory
from fastapi import HTTPException
import random


async def get_item(items, uid, group_id):
    async with get_session() as session:
        user = await session.execute(select(User).filter_by(user_id=uid))
        user_id = user.scalar_one_or_none()

        if not user_id:
            raise HTTPException(status_code=400, detail="User not found")

        rarity = await session.execute(
            select(RarityCategory).filter_by(ext_id=group_id)
        )
        rarity_id = rarity.scalar_one_or_none()

        user_percent = float(user_id.individual_percent)
        rarity_percent = float(rarity_id.category_percent)

        coeff_for_all_objects = rarity_percent / len(items)

        coefficients = []
        for item in items:
            coef = await session.execute(
                select(Item).filter_by(item_id=item["item_id"])
            )

            if not coef:
                return HTTPException(
                    status_code=404,
                    detail="Внутренняя ошибка сервера обратитесь к Технической поддержке",
                )

            coef_id = coef.scalar_one_or_none()

            coef_item = coef_id.step_down_factor

            if user_percent is None:
                user_percent = 1.0
            if rarity_percent is None:
                rarity_percent = 1.0
            if coef_item is None:
                coef_item = 1.0

            coefficients.append(
                float(coeff_for_all_objects) * float(coef_item) * float(user_percent)
            )

        item = random.choices(items, coefficients)

        return item
