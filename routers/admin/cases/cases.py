from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from security import verify_admin
from models.case_schemas import (
    AdminCaseSchema,
    AdminCreateCaseSchema,
    AdminListCasesSchema,
)
from models.schemas import SuccessResponse
from .functions import _create_case_items, get_cases

router = APIRouter()


@router.post(
    "/case/create",
    response_model=AdminCaseSchema,
    responses={400: {"model": SuccessResponse}},
)
async def create_case_list(case: AdminCreateCaseSchema, admin=Depends(verify_admin)):
    try:
        case_ = await _create_case_items(case=case.model_dump())
    except ValueError as error:
        return JSONResponse(
            {"message": error.args},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return case_


@router.get("/cases", response_model=AdminListCasesSchema)
async def get_all_cases(
    page: int = 0, page_size: int = 20, admin: str = Depends(verify_admin)
):
    cases = await get_cases(page=page, page_size=page_size)
    if not cases:
        raise HTTPException(status_code=404, detail="No cases found")
    return cases
