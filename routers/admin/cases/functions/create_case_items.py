from sqlalchemy import select
from database import get_session
from models import Case, Category
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException, status
from routers.admin.items.functions import get_item
from .get_case_module import get_case_by_name
import base64
import aiofiles
import os

PATH = f"""{os.path.abspath("images/cases")}"""


async def _create_case_items(case: dict):
    async with get_session() as session:
        items = case.pop("items")

        file_path = f"{PATH}/{case.pop('image_name')}"

        category_id = case.get("category_id")
        name = case.get("name")
        created = await get_case_by_name(name)
        if created:
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Кейс с таким именем уже существует",
            )

        try:
            category = await session.execute(
                select(Category).filter_by(category_id=category_id)
            )
            category = category.scalars().one()
        except NoResultFound:
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Категория {category_id} не найденa!",
            )

        async with aiofiles.open(file_path, "wb") as f:
            await f.write(base64.b64decode(case["image"]))

        case["image"] = file_path

        case = Case(**case)

        case.items = [await get_item(item_id=item["item_id"]) for item in items]

        session.add(case)
        await session.commit()
        await session.flush(case)
        await session.refresh(case, attribute_names=('category', 'items'))

    return case
