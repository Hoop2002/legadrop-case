from fastapi import APIRouter, HTTPException
from .functions import get_cases
from typing import List
from models import ResponceCase

router = APIRouter()


@router.get("/cases")
async def get_all_cases():
    cases = await get_cases()
    if not cases:
        raise HTTPException(status_code=404, detail="No cases found")
    return cases
