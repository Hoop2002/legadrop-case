from sqlalchemy.future import select
from database import get_session
from models import UserData, User


async def get_user( user_id: str ) -> UserData:
	async with get_session() as session:
		result = await session.execute(select(User).filter_by(user_id=user_id))
		user = result.scalar_one_or_none()
	return user


async def get_user_by_username( username: str ) -> UserData:
	async with get_session() as session:
		result = await session.execute(select(User).filter_by(username=username))
		user = result.scalar_one_or_none()
	return user


async def get_user_by_email( email: str ) -> UserData:
	async with get_session() as session:
		result = await session.execute(select(User).filter_by(email=email))
		user = result.scalar_one_or_none()
	return user


