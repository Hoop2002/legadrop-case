from database import get_session
from models import GoogleAuth, SocialAuth


async def auth_google(social_data: GoogleAuth):
    async with get_session() as session:
        social_data = SocialAuth(**social_data.model_dump())
        session.add(social_data)
        return social_data
