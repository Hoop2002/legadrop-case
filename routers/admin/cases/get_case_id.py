from fastapi import APIRouter, HTTPException, status
from .functions import get_case_by_name
from models import RequestCaseName


router = APIRouter()


@router.delete("/case")
async def get_case_(data: RequestCaseName):
    case_data = await get_case_by_name(name=data.name)
    if not case_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Кейс не найден"
        )
    return case_data
