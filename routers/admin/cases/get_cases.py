from fastapi import APIRouter, Depends, HTTPException
from .functions import get_cases
from typing import List
from models import ResponceCase
from security import verify_admin

router = APIRouter()


@router.get("/cases")
async def get_all_cases(admin: str = Depends(verify_admin)):
    cases = await get_cases()
    if not cases:
        raise HTTPException(status_code=404, detail="No cases found")
    return cases
