from sqladmin import ModelView

from .models import (
    Role,
    Permission,
    Administrator,
    Case,
    ItemCompound,
    RarityCategory,
    Item,
    User,
    SocialAuth,
    Deposit,
    Expenditure,
    UserToken,
    Test,
    AdminPanelUser,
    ItemsFindings,
    ItemsFindingsStatus,
)


class UserAdmin(ModelView, model=User):
    column_list = "__all__"


class SocialAuthAdmin(ModelView, model=SocialAuth):
    column_list = "__all__"


class DepositAdmin(ModelView, model=Deposit):
    column_list = "__all__"


class ExpenditureAdmin(ModelView, model=Expenditure):
    column_list = "__all__"


class UserTokenAdmin(ModelView, model=UserToken):
    column_list = "__all__"


class ItemCompoundAdmin(ModelView, model=ItemCompound):
    column_list = "__all__"


class TestAdmin(ModelView, model=Test):
    column_list = "__all__"


class RoleAdmin(ModelView, model=Role):
    column_list = "__all__"


class PermissionAdmin(ModelView, model=Permission):
    column_list = "__all__"


class AdministratorAdmin(ModelView, model=Administrator):
    column_list = "__all__"


class RarityCategoryAdmin(ModelView, model=RarityCategory):
    column_list = "__all__"


class CaseAdmin(ModelView, model=Case):
    column_list = "__all__"


class ItemAdmin(ModelView, model=Item):
    column_list = "__all__"


class AdminPanelUserAdmin(ModelView, model=AdminPanelUser):
    column_list = "__all__"


class AdminItemsFindings(ModelView, model=ItemsFindings):
    column_list = "__all__"


class AdminItemsFindingsStatus(ModelView, model=ItemsFindingsStatus):
    column_list = "__all__"
