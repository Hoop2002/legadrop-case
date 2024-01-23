from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from models.promo_schemas import UserRequestPromoCodeSchema
from models.schemas import SuccessResponse
from security.token_functions import verify_user
from routers.admin.promocodes.functions import get_promo, used_promo

router = APIRouter()


@router.post("/user/activate_promo", response_model=SuccessResponse, responses={400: {'model': SuccessResponse}})
async def activate_promo(promo_code: UserRequestPromoCodeSchema, user_id: str = Depends(verify_user)) -> JSONResponse:
    used = await used_promo(code_data=promo_code.code_data, user_id=user_id)
    if used:
        return JSONResponse(
            {'message': 'Вы уже использовали этот промокод'}, status_code=status.HTTP_400_BAD_REQUEST
        )
    promo = await get_promo(filter_by={'code_data': promo_code.code_data, 'active': True})
    if len(promo) == 0:
        return JSONResponse(
            {'message': 'Промокод недействителен'}, status_code=status.HTTP_400_BAD_REQUEST
        )
    promo = promo[0]
    await promo.activate_pomo(user_id)
    return JSONResponse(
        {'message': 'Промокод успешно использован'}, status_code=status.HTTP_202_ACCEPTED
    )
