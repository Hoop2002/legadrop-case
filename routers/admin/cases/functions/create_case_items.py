from sqlalchemy import select
from database import get_session
from models import Case, Item, Category
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException, status
from models.models import case_items
from routers.admin.items.functions import get_item
import base64
import aiofiles
import os

PATH = f"""{os.path.abspath("images/cases")}"""

async def _create_case_items(case):
    async with get_session() as session:
        items = case.pop("items")

        file_path = f"{PATH}/{case['image_name']}"

        category_id = case.get("category")
        name = case.get("name")

        try:
            category = await session.execute(select(Category).filter_by(category_id=category_id))
            category = category.scalars().one()
        except NoResultFound:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Категория {category_id} не найденa!")
        
        async with aiofiles.open(file_path,'wb') as f:
            await f.write(base64.b64decode(case['image']))
        
        case = Case(name=name, image=file_path, category_id=category_id)
        
        case.items = [await get_item(item_id=item["item_id"]) for item in items]
        
        session.add(case)
        await session.commit()
        await session.flush(case)

    return case