from fastapi import APIRouter, HTTPException, status, Depends
from .functions import delete_case
from models import RequestCase
from security import verify_admin

router = APIRouter()


@router.delete("/case")
async def get_case_(data: RequestCase, admin: str = Depends(verify_admin)):
    case_data = await delete_case(case_id=data.case_id)
    if not case_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Кейс не найден"
        )
    return {"status": "success", "message": "Case deleted successfully"}
