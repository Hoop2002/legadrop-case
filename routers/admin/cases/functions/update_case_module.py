from sqlalchemy import select
from typing import Optional
from database import get_session
from models import Case


async def update_case(case_id: str, **kwargs) -> Optional[Case]:
    async with get_session() as session:
        result = await session.execute(select(Case).filter_by(case_id=case_id))
        case = result.scalars().first()
        if not case:
            return None
        
        if "name" in kwargs:
            case.name = kwargs["name"]
        if "image" in kwargs:
            case.image = kwargs["image"]
        if "cost" in kwargs:
            case.cost = kwargs["cost"]
        if "category_id" in kwargs:
            case.category_id = kwargs["category_id"]
        
        await session.commit()
        await session.refresh(case)
        return case


