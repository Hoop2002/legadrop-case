from fastapi import APIRouter, HTTPException, Depends, status
from .functions import get_case
from models import RequestCase
from security import verify_admin

router = APIRouter()


@router.get("/case")
async def get_case_(data: RequestCase, admin: str = Depends(verify_admin)):
    case_data = await get_case(case_id=data.case_id)
    if not case_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Кeйс не найден"
        )
    return case_data
