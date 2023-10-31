from fastapi import HTTPException, status
from sqlalchemy.future import select
from database import get_session
from models import Administrator, AdminUpdate

async def update_employee(admin_id: str, update_model: AdminUpdate) -> bool:
    update_data = update_model.model_dump(exclude_unset=True)
    async with get_session() as session:
        try:
            result = await session.execute(select(Administrator).filter_by(admin_id=admin_id))
            admin = result.scalar_one_or_none()
            if not admin:
                return False

            for key, value in update_data.items():
                setattr(admin, key, value)
            return True

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
