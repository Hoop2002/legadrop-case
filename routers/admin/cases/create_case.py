from fastapi import APIRouter, HTTPException, status, UploadFile, Form, File, Depends
from pathlib import Path
from .functions import create_case, get_case_by_name
from security import verify_admin

router = APIRouter()

IMAGES_PATH = "images/cases"


@router.post("/case")
async def create_case_(
    name: str = Form(...),
    category_id: str = Form(...),
    image: UploadFile = File(...),
    admin: str = Depends(verify_admin),
):
    case = await get_case_by_name(name)
    if case:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Кейс уже существует"
        )

    image_path = Path(IMAGES_PATH) / f"{name}.jpg"
    with image_path.open("wb") as buffer:
        content = await image.read()
        buffer.write(content)

    image_path = f"images/case/{name}.jpg"
    case = await create_case(name=name, image=str(image_path), category_id=category_id)

    return case


from models.request_models import CreateCases
from .functions import _create_case_items


@router.post("/case/create")
async def create_case_list(case: CreateCases):
    case_ = await _create_case_items(case=case.model_dump())
    return case_
