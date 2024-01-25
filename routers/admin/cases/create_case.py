from fastapi import APIRouter, Depends
from security import verify_admin
from models.case_schemas import AdminCaseSchema, AdminCreateCaseSchema
from .functions import _create_case_items

router = APIRouter()


@router.post("/case/create")
async def create_case_list(case: AdminCreateCaseSchema, admin=Depends(verify_admin)):
    case_ = await _create_case_items(case=case.model_dump())
    return case_
