from database import get_session
from models import User, UserSignUp


async def auth(user_data: UserSignUp) -> User:
    async with get_session() as session:
        created_user = User(**user_data.model_dump())
        session.add(created_user)
        await session.commit()
        return created_user
