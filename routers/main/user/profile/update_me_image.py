from fastapi import APIRouter, HTTPException, status, UploadFile, File, Depends
from security.token_functions import verify_user
from utils import update_user_image
from .functions import update_me_image


router = APIRouter()


@router.put("/user/me/image")
async def update_me_image_(
    image: UploadFile = File(...), user_id=Depends(verify_user)
):
    path = await update_user_image(image_name=user_id, upload_image=image)
    user_data = await update_me_image(user_id=user_id, path=str(path))
    return user_data
