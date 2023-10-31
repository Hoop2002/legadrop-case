from database import get_session
from models import Administrator, AdminCreate


async def create_employee( admin_data: AdminCreate ):
	async with get_session() as session:
		created_employee = Administrator(**admin_data.model_dump())
		session.add(created_employee)
		await session.commit()
		await session.flush()
	return created_employee
