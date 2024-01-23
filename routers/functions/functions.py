from typing import Optional
from sqlalchemy import select, update
from database import get_session
from models import User


async def get_user(user_id: str) -> Optional[User]:
    async with get_session() as session:
        stmt = select(User).filter_by(user_id=user_id)
        result = await session.execute(stmt)
        user = result.scalars().first()
        return user
