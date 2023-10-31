from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from database import get_session
from models import User, Item

async def open_case(user_id: int, item_id: int):
    async with get_session() as session:
        result_user = await session.execute(
            select(User).options(joinedload(User.inventory_items)).where(User.id == user_id)
        )
        user = result_user.scalars().first()
        
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Пользователь с ID '{user_id}' не найден!")
        
        # Получаем предмет по item_id из базы данных
        result_item = await session.execute(
            select(Item).where(Item.id == item_id)
        )
        item = result_item.scalars().first()
        
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Предмет с ID '{item_id}' не найден!")
        
        if item not in user.inventory_items:
            user.inventory_items.append(item)
        
        await session.commit()
        
        return user, item
