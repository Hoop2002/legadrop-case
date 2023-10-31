from fastapi import APIRouter
from .functions import delete_case_item
from models import RequestCaseItemDelete

router = APIRouter()


@router.delete("/case/item")
async def delete_case_item_(data: RequestCaseItemDelete):
    case, item = await delete_case_item(case_id=data.case_id, item_id=data.item_id)

    return {
        "status": "success",
        "message": f"Предмет '{item.name}' успешно удален из кейса '{case.name}'",
    }
