from fastapi import HTTPException, status
from database import get_session
from .get_case_items_module import get_case_items
from routers.admin.items.functions import get_item
from models import Item, Case
from models.models import case_items
from sqlalchemy import delete

async def delete_case_item(case_id: str, item_id: str):
    async with get_session() as session:
        case = await get_case_items(case_id=case_id)
        if not case:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Кейс с ID '{case_id}' не найден!")

        item = await get_item(item_id=item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Предмет с ID '{item_id}' не найден!")

        if item in case.items:
            case.items.remove(item)
        
        
        await session.commit()

        return case, item
    
async def _delete_case_items(case_id: str, items: list):
    async with get_session() as session:
        not_found_items = []
        delete_items = []
        delete_items_return = []
        case = await get_case_items(case_id=case_id)
        if not case:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Кейс с ID '{case_id}' не найден!")
        
        for item in items:
            item_obj = await get_item(item_id=item)

            if not item_obj:
                not_found_items.append(item)
                break
            else:
                stmt = (
                    delete(case_items).
                    filter_by(case_id=case_id, item_id=item)
                )
                await session.execute(stmt)

                delete_items_return.append(item_obj)
        
        await session.commit()
        
        return delete_items_return, not_found_items, case
