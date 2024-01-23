from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from security import verify_admin
from models import RequestAdminID
from models.promo_schemas import PromoCodeRequestSchema, ListPromoCodesSchema


router = APIRouter()


@router.get('/promo', response_model=ListPromoCodesSchema)
async def get_promo_codes(admin: RequestAdminID = Depends(verify_admin)):
    pass


@router.post('/promo/create_promo')
async def create_promo_code(promo: PromoCodeRequestSchema, admin: RequestAdminID = Depends(verify_admin)):
    pass
