from fastapi import HTTPException, APIRouter, status, Depends
from models.request_models import OutputAllItemF
from .func import (
    create_output_,
    get_outputs,
    get_output_,
    delete_output_,
    inactive_output,
)
from security import verify_admin

router = APIRouter()


@router.post("/api/v1/output/create")
async def create_outputs(data: OutputAllItemF, admin: str = Depends(verify_admin)):
    outputs = await create_output_(outputs=data.model_dump())
    return outputs


@router.get("/api/v1/output/")
async def gets_outputs(
    page_size: int = None, page: int = None, admin: str = Depends(verify_admin)
):
    output = await get_outputs(page_size=page_size, page=page)
    return output


@router.get("/api/v1/output/{itemfs_id}")
async def get_output(itemfs_id: str, admin: str = Depends(verify_admin)):
    output = await get_output_(itemfs_id=itemfs_id)
    return output


# @router.delete("/api/v1/output/delete/{itemfs_id}")
# async def delete_output(itemfs_id: str):
#    del_output = await delete_output_(itemfs_id=itemfs_id)
#    return del_output


@router.put("/api/v1/output/{itemsf_id}/cancelled")
async def output_inactive(itemsf_id, admin: str = Depends(verify_admin)):
    in_itemfs = await inactive_output(itemsf_id=itemsf_id)
    return in_itemfs


async def update_status():
    pass
