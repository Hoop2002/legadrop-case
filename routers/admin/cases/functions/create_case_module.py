from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select
from database import get_session
from models import Case, Category

async def create_case(name: str, image: str, category_id: str) -> Case:
    async with get_session() as session:
        # Проверка существования категории с указанным category_id
        try:
            category = await session.execute(select(Category).filter_by(category_id=category_id))
            category = category.scalars().one()
        except NoResultFound:
            raise ValueError(f"Category with ID {category_id} not found")
        
        # Создание нового объекта Case
        case = Case(name=name, image=image, category_id=category_id)
        
        session.add(case)
        await session.commit()
        await session.refresh(case)
        
        return case
