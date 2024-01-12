from fastapi import APIRouter, HTTPException, status, Request
from models import RequestItemUpdate, ResponseItem
from .functions import get_case, _update_case

router = APIRouter()


@router.put("/case/update")
async def update_case(data: dict):
    if not data.get("case_id", False):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="key 'case_id' not found"
        )

    case = await get_case(case_id=data.get("case_id"))

    if not case:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Кейс не найден!"
        )

    case = await _update_case(data)

    return case
