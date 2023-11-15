from database import get_session
from models import User, UserCreate


async def create_user(user_data: UserCreate) -> User:
    async with get_session() as session:
        created_user = User(**user_data.model_dump())
        print(create_user)
        session.add(created_user)
        await session.commit()

    return created_user


# async def create_user(user_data: dict):
#     """Создание нового пользователя."""
#     async with get_session() as session:
#         user = User(**user_data)
#         session.add(user)
#         await session.commit()