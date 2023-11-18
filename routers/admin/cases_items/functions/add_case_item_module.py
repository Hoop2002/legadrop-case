from fastapi import HTTPException, status
from database import get_session
from .get_case_items_module import get_case_items
from routers.admin.items.functions import get_item
from models import Case, Item
from models.models import case_items
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select, update

async def add_case_item(case_id: str, item_id: str):
    async with get_session() as session:
        case = await get_case_items(case_id=case_id)
        if not case:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Кейс с ID '{case_id}' не найден!",
            )

        item = await get_item(item_id=item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Предмет с ID '{item_id}' не найден!",
            )

        # Check if the item is already in the case by item ID
        if not any(i.item_id == item.item_id for i in case.items):
            case.items.append(item)

        # Add the case back to the session
        session.add(case)
        await session.commit()

        return case, item

async def _add_items_in_case(case):
    async with get_session() as session:
        case_id = case.get("case_id")
        items_ = case.pop("items")
        try:

            case_ = await session.execute(select(Case).filter_by(case_id=case_id))
            case_obj = case_.scalar_one_or_none()
            
            for item in items_:
                item_ = await session.execute(select(Item).filter_by(item_id=item['item_id']))
                item_obj = item_.scalar_one_or_none()
                
                await session.execute(case_items.insert(), [{'case_id': case_obj.case_id, "item_id": item_obj.item_id}])
            await session.commit()
            case["items"] = items_
            
            return case
        except NoResultFound:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Категория {case_id} не найденa!")
        
        