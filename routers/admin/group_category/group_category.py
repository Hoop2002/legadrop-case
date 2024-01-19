from ssl import DER_cert_to_PEM_cert
from unicodedata import category
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import select
from typing import Optional
from database import get_session
from models import RarityCategory, RarityCategoryUPD
from security import verify_admin

router = APIRouter()


@router.get("/group_category")
async def get_group_category(admin: str = Depends(verify_admin)):
    async with get_session() as session:
        rarity = await session.execute(select(RarityCategory))
        rarity_sc = rarity.scalars().all()

        return rarity_sc


@router.post("/group_category/update")
async def rarity_update(data: RarityCategoryUPD):
    kw = data.model_dump()

    async with get_session() as session:
        data = data.model_dump()

        rarity = await session.execute(
            select(RarityCategory).filter_by(category_id=data["rarity_id"])
        )
        rarity_sc = rarity.scalar_one_or_none()

        if not rarity_sc:
            return HTTPException(
                status_code=404, detail="Категория редкости не найдена!"
            )

        rarity_sc.category_percent = kw["category_percent"]
        rarity_sc.name = kw["name"]

        await session.commit()

        return rarity_sc
