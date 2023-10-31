from fastapi import APIRouter
from .functions import add_case_item
from models import RequestAddCaseItem

router = APIRouter()


@router.post("/case/item")
async def add_case_item_(data: RequestAddCaseItem):
    case, item = await add_case_item(case_id=data.case_id, item_id=data.item_id)

    return {"message": f"Предмет '{item.name}' успешно добавлен в кейс '{case.name}'"}
