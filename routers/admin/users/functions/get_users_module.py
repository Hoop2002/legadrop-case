from sqlalchemy.future import select
from typing import List
from database import get_session
from models import User, UserData


async def get_users() -> List[UserData]:
	async with get_session() as session:
		result = session.execute(select(User))
		users = result.scalars().all()
		return [UserData(user) for user in users]
