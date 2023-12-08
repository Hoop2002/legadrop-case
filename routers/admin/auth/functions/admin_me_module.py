from sqlalchemy.future import select
from typing import Union
from database import get_session
from models import AdminMe, Administrator


async def me(admin_id: str) -> Union[AdminMe, None]:
    async with get_session() as session:
        statement = select(Administrator).filter_by(admin_id=admin_id)
        result = session.execute(statement)
        admin = result.fetchone()

        if admin:
            admin_data = AdminMe.from_orm(admin)
            return admin_data
        else:
            return None
