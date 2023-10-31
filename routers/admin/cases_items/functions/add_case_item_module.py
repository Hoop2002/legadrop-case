from fastapi import HTTPException, status
from database import get_session
from .get_case_items_module import get_case_items
from routers.admin.items.functions import get_item


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
