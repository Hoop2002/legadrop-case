from fastapi import APIRouter, HTTPException, status
from .functions import delete_case_item, _delete_case_items
from models import RequestCaseItemDelete

router = APIRouter()


@router.delete("/case/item")
async def delete_case_item_(data: RequestCaseItemDelete):
    case, item = await delete_case_item(case_id=data.case_id, item_id=data.item_id)

    return {
        "status": "success",
        "message": f"Предмет '{item.name}' успешно удален из кейса '{case.name}'",
    }


@router.delete("/case/item/delete")
async def delete_case_items(data: dict):
    if not data.get("case_id", False):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="key 'case_id' not found"
        )
    if not data.get("items", False):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="key 'items' not found"
        )

    items, not_found_items, case = await _delete_case_items(
        case_id=data["case_id"], items=data["items"]
    )

    return {
        "status": "success",
        "message": f"Предметы {', '.join(x.name for x in items if x)} успешно удалены из кейса '{case.name}'",
        "not_found_items": [x for x in not_found_items],
    }
