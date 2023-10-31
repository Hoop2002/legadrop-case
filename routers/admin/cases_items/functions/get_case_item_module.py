from fastapi import HTTPException, status
from typing import Optional
from .get_case_items_module import get_case_items
from models import Item

async def get_case_item(case_id: str, item_id: str) -> Optional[Item]:
    case = await get_case_items(case_id)
    if not case:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Кейс с ID '{case_id}' не найден!")

    for item in case.items:
        if item.item_id == item_id:
            return item

    return None
