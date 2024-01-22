from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from uvicorn import run
from dotenv import load_dotenv

load_dotenv()

from routers.admin.auth import admin_sign_in, admin_me

from routers.admin.permissions import (
    create_permission,
    get_permissions,
    get_permission_id,
    get_permission,
)

from routers.admin.roles import create_role, get_roles, get_role

from routers.admin.assign import (
    assign_permission,
    get_role_permissions,
    get_permission_roles,
    assign_role,
)

from routers.admin.employees import (
    create_employee,
    get_employees,
    get_employee,
    delete_employee,
)

from routers.admin.categories import (
    create_category,
    get_categories,
    get_category,
    get_category_id,
    update_category,
    delete_category,
)

from routers.admin.cases import (
    create_case,
    get_cases,
    get_case,
    delete_case,
    update_case,
)
from routers.admin.items import (
    create_item,
    get_items,
    get_item,
    get_item_id,
    update_item,
    delete_item,
)

from routers.admin.cases_items import (
    add_case_item,
    get_cases_items,
    get_case_items,
    get_case_item,
    delete_case_item,
)

from routers.admin.users import create_user

from routers.main.user.profile import (
    user_me,
    update_me_username,
    update_me_email,
    update_me_locale,
    update_me_image,
    change_password,
)
from routers.main.user.items import get_user_items
from routers.main.shop import shop

from routers.admin.group_category import rarity_group

from routers.main.auth import user_sign_up, user_sign_in, user_auth_google

from routers.spec import password_generator

from routers.main.case import opening_case

from routers.integration.moogold import moogold_api

from routers.admin.outputs import output_api

app = FastAPI(
    title="Legadrop API",
    description="API LEGADROP",
    version="0.1.5",
)

# Добавление middleware для CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешает все источники
    allow_credentials=True,
    allow_methods=["*"],  # Разрешает все методы
    allow_headers=["*"],  # Разрешает все заголовки
)


app.mount("/images", StaticFiles(directory="images/"), name="images")


app.include_router(
    opening_case, tags=["randomaizer/opening_case"], prefix="/randomaizer"
)

app.include_router(admin_sign_in, tags=["admin"], prefix="/admin")
app.include_router(admin_me, tags=["admin"], prefix="/admin")
app.include_router(create_employee, tags=["admin"], prefix="/admin")
app.include_router(get_employees, tags=["admin"], prefix="/admin")
app.include_router(get_employee, tags=["admin"], prefix="/admin")
app.include_router(delete_employee, tags=["admin"], prefix="/admin")

app.include_router(assign_permission, tags=["admin/assign"], prefix="/admin")
app.include_router(get_role_permissions, tags=["admin/assign"], prefix="/admin")
app.include_router(get_permission_roles, tags=["admin/assign"], prefix="/admin")
app.include_router(assign_role, tags=["admin/assign"], prefix="/admin")

app.include_router(create_user, tags=["admin"], prefix="/admin")
app.include_router(create_role, tags=["admin/roles"], prefix="/admin")
app.include_router(get_roles, tags=["admin/roles"], prefix="/admin")
app.include_router(get_role, tags=["admin/roles"], prefix="/admin")
app.include_router(create_permission, tags=["admin/permissions"], prefix="/admin")
app.include_router(get_permissions, tags=["admin/permissions"], prefix="/admin")
app.include_router(get_permission_id, tags=["admin/permissions"], prefix="/admin")
app.include_router(get_permission, tags=["admin/permissions"], prefix="/admin")

app.include_router(create_category, tags=["admin/categories"], prefix="/admin")
app.include_router(get_categories, tags=["admin/categories"], prefix="/admin")
app.include_router(get_category, tags=["admin/categories"], prefix="/admin")
app.include_router(get_category_id, tags=["admin/categories"], prefix="/admin")
app.include_router(update_category, tags=["admin/categories"], prefix="/admin")
app.include_router(delete_category, tags=["admin/categories"], prefix="/admin")

app.include_router(create_case, tags=["admin/cases"], prefix="/admin")
app.include_router(get_cases, tags=["admin/cases"], prefix="/admin")
app.include_router(get_case, tags=["admin/cases"], prefix="/admin")
app.include_router(update_case, tags=["admin/cases"], prefix="/admin")
app.include_router(delete_case, tags=["admin/cases"], prefix="/admin")

app.include_router(rarity_group, tags=["admin/rarity"], prefix="/admin")

app.include_router(create_item, tags=["admin/items"], prefix="/admin")
app.include_router(get_items, tags=["admin/items"], prefix="/admin")
app.include_router(get_item, tags=["admin/items"], prefix="/admin")
app.include_router(get_item_id, tags=["admin/items"], prefix="/admin")
app.include_router(update_item, tags=["admin/items"], prefix="/admin")
app.include_router(delete_item, tags=["admin/items"], prefix="/admin")


app.include_router(add_case_item, tags=["admin/case/items"], prefix="/admin")
app.include_router(get_cases_items, tags=["admin/case/items"], prefix="/admin")
app.include_router(get_case_items, tags=["admin/case/items"], prefix="/admin")
app.include_router(get_case_item, tags=["admin/case/items"], prefix="/admin")
app.include_router(delete_case_item, tags=["admin/case/items"], prefix="/admin")


app.include_router(user_sign_up, tags=["main"])
app.include_router(user_sign_in, tags=["main"])
app.include_router(user_auth_google, tags=["main"])

app.include_router(user_me, tags=["main"])
app.include_router(update_me_username, tags=["main"])
app.include_router(update_me_email, tags=["main"])
app.include_router(update_me_locale, tags=["main"])
app.include_router(update_me_image, tags=["main"])
app.include_router(change_password, tags=["main"])
app.include_router(get_user_items, tags=["main"])
app.include_router(shop, tags=["main"])


app.include_router(password_generator, tags=["spec"], prefix="/admin/spec")

app.include_router(moogold_api, tags=["moogold/api"])

app.include_router(output_api, tags=["output/users/api"])

from sqladmin import Admin
from database.database import engine

from models.admins_models import (
    RoleAdmin,
    PermissionAdmin,
    AdministratorAdmin,
    RarityCategoryAdmin,
    CaseAdmin,
    ItemAdmin,
    ItemCompoundAdmin,
    UserAdmin,
    SocialAuthAdmin,
    DepositAdmin,
    ExpenditureAdmin,
    UserTokenAdmin,
    AdminPanelUserAdmin,
    AdminItemsFindings,
    AdminItemsFindingsStatus,
)

from admin_back_auth import AdminAuth

back_auth = AdminAuth(secret_key="admin")

admin = Admin(app, engine, authentication_backend=back_auth, base_url="/admin_panel")

admin.add_view(RoleAdmin)
admin.add_view(PermissionAdmin)
admin.add_view(AdministratorAdmin)
admin.add_view(RarityCategoryAdmin)
admin.add_view(CaseAdmin)
admin.add_view(ItemAdmin)
admin.add_view(ItemCompoundAdmin)
admin.add_view(UserAdmin)
admin.add_view(SocialAuthAdmin)
admin.add_view(DepositAdmin)
admin.add_view(ExpenditureAdmin)
admin.add_view(UserTokenAdmin)
admin.add_view(AdminPanelUserAdmin)
admin.add_view(AdminItemsFindings)
admin.add_view(AdminItemsFindingsStatus)


if __name__ == "__main__":
    run("main:app", host="127.0.0.1", port=8000, reload=True)
