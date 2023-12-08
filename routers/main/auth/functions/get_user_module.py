from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from typing import Union
from database import get_session
from models import User, SocialAuth, UserData


async def _get_user_by_field(field_name: str, value: str) -> Union[UserData, None]:
    async with get_session() as session:
        try:
            result = await session.execute(
                select(User).filter_by(**{field_name: value})
            )
            user_data = result.scalar_one_or_none()
            return user_data
        except NoResultFound:
            return None


async def get_user(user_id: str) -> Union[UserData, None]:
    return await _get_user_by_field(field_name="user_id", value=user_id)


async def get_user_by_username(username: str) -> Union[UserData, None]:
    return await _get_user_by_field(field_name="username", value=username)


async def get_user_by_email(email: str) -> Union[UserData, None]:
    return await _get_user_by_field(field_name="email", value=email)


async def get_user_by_social_id(social_id: str) -> Union[User, None]:
    async with get_session() as session:
        statement = (
            select(User)
            .join(SocialAuth, User.user_id == SocialAuth.user_id)
            .filter(SocialAuth.social_id == social_id)
        )
        try:
            result = await session.execute(statement)
            user_data = await result.scalar_one()  # type: ignore
            return user_data
        except NoResultFound:
            return None
