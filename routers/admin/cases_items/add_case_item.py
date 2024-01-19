from fastapi import APIRouter, Depends
from .functions import add_case_item
from .functions import _add_items_in_case
from models import RequestAddCaseItem
from models.request_models import AddItemsInOneCase
from security import verify_admin

router = APIRouter()


@router.post("/case/item")
async def add_case_item_(data: RequestAddCaseItem, admin: str = Depends(verify_admin)):
    case, item = await add_case_item(case_id=data.case_id, item_id=data.item_id)

    return {"message": f"Предмет '{item.name}' успешно добавлен в кейс '{case.name}'"}


@router.post("/case/add/items/list")
async def add_items_in_case(
    case: AddItemsInOneCase, admin: str = Depends(verify_admin)
):
    case_ = await _add_items_in_case(case.model_dump())
    return case_
