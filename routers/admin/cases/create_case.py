from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from security import verify_admin
from models.case_schemas import AdminCaseSchema, AdminCreateCaseSchema
from models.schemas import SuccessResponse
from .functions import _create_case_items

router = APIRouter()


@router.post("/case/create", response_model=AdminCaseSchema, responses={400: {'model':  SuccessResponse}})
async def create_case_list(case: AdminCreateCaseSchema, admin=Depends(verify_admin)):
    try:
        case_ = await _create_case_items(case=case.model_dump())
    except ValueError as error:
        return JSONResponse(
            {'message': error.args},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return case_
