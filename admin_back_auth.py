from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from database import get_session
from models.models import AdminPanelUser
from sqlalchemy.future import select


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        if not username:
            return False
        if not password:
            return False

        # Validate username/password credentials
        # And update session
        async with get_session() as session:
            try:
                admin_user = await session.execute(
                    select(AdminPanelUser).filter_by(login=username)
                )
                admin = admin_user.scalars().one()
                # print(admin)
                if password == admin.password:
                    request.session.update({"token": admin.token})
                    return True
                else:
                    return False
            except:
                return False

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        # Check the token in depth
        return True
