from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from security import verify_admin
from models import RequestAdminID, PromoCode
from models.promo_schemas import PromoCodeRequestSchema, ListPromoCodesSchema, PromoCodeResponseSchema
from .functions import get_promo


router = APIRouter()


@router.get("/promo", response_model=ListPromoCodesSchema)
async def get_promo_codes(page: int = 0, page_size: int = 20, admin: RequestAdminID = Depends(verify_admin)):
    promo_codes = await get_promo(page_size=page_size, page=page)
    return promo_codes


@router.get("/promo/{promo_id}", response_model=PromoCodeResponseSchema)
async def get_promo_code(promo_id: int, admin: RequestAdminID = Depends(verify_admin)):
    promo_code = await get_promo(filter_by=dict(id=promo_id))
    promo_code = promo_code[0]
    if not promo_code:
        return JSONResponse({
            "message": "Такой промокод не найден"
        }, status_code=status.HTTP_400_BAD_REQUEST)
    return promo_code


@router.post("/promo/create_promo", response_model=PromoCodeResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_promo_code(
    promo_data: PromoCodeRequestSchema, admin: RequestAdminID = Depends(verify_admin)
):
    new_promo = await PromoCode.create(**promo_data.model_dump())
    return new_promo
