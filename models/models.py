from datetime import datetime
from typing import List
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    DECIMAL,
    ForeignKey,
    Integer,
    String,
    Table,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database import Base, get_session
from utils import generator_id


role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", String, ForeignKey("roles.role_id"), primary_key=True),
    Column(
        "permission_id",
        String,
        ForeignKey("permissions.permission_id"),
        primary_key=True,
    ),
)

admin_roles = Table(
    "admin_roles",
    Base.metadata,
    Column("role_id", String, ForeignKey("roles.role_id"), primary_key=True),
    Column("admin_id", String, ForeignKey("administrators.admin_id"), primary_key=True),
)


class AdminPanelUser(Base):
    __tablename__ = "admin_panel_user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String, unique=True)
    password = Column(String)
    token = Column(String, unique=True)


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_id = Column(String, unique=True, default=generator_id)
    name = Column(String, unique=True)
    permissions = relationship(
        "Permission", secondary=role_permissions, back_populates="roles"
    )
    administrators = relationship(
        "Administrator", secondary=admin_roles, back_populates="roles"
    )


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    permission_id = Column(String, unique=True, default=generator_id)
    name = Column(String)
    roles = relationship(
        "Role", secondary=role_permissions, back_populates="permissions"
    )


class Administrator(Base):
    __tablename__ = "administrators"

    id = Column(Integer, primary_key=True, autoincrement=True)
    admin_id = Column(String, unique=True, default=generator_id)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    password_hash = Column(String)
    image = Column(String)
    date_created = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)
    roles = relationship("Role", secondary=admin_roles, back_populates="administrators")


case_items = Table(
    "case_items",
    Base.metadata,
    Column("case_id", String, ForeignKey("cases.case_id"), primary_key=True),
    Column("item_id", String, ForeignKey("items.item_id"), primary_key=True),
)

case_openings = Table(
    "case_openings",
    Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", String, ForeignKey("users.user_id")),
    Column("case_id", String, ForeignKey("cases.case_id")),
    Column("opened_date", DateTime, default=datetime.utcnow),
)


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(String, unique=True, default=generator_id)
    name = Column(String)
    cases = relationship("Case", back_populates="category", lazy="dynamic")


class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, autoincrement=True)
    case_id = Column(String, unique=True, default=generator_id)
    name = Column(String)
    image = Column(String)
    category_id = Column(String, ForeignKey("categories.category_id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    category = relationship("Category", back_populates="cases")
    items = relationship("Item", secondary=case_items, back_populates="cases")
    user_opened = relationship(
        "User", secondary=case_openings, back_populates="opened_cases"
    )


class ItemCompound(Base):
    __tablename__ = "item_compounds"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    quantity = Column(Integer)
    item_id = Column(String, ForeignKey("items.item_id"))
    moogold_id = Column(String)
    test = Column(String)
    item = relationship("Item", back_populates="compound")


class RarityCategory(Base):
    __tablename__ = "rarity_category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    category_id = Column(String, unique=True, default=generator_id)
    category_percent = Column(DECIMAL, nullable=False)  # групповой процент
    item: Mapped[List["Item"]] = relationship("Item", back_populates="rarity_category")
    ext_id = Column(String, unique=True)


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(String, unique=True, default=generator_id)
    name = Column(String, nullable=False)
    cost = Column(DECIMAL)
    cost_in_rubles = Column(DECIMAL, nullable=False, default=0)
    sale = Column(Boolean, default=True, nullable=False)  # предмет продаётся
    # active = Column(Boolean, default=True)  # Предмет можно юзать в кейсе
    gem_cost = Column(Integer)  # todo скорее всего стоит удалить
    color = Column(String)
    image = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    step_down_factor = Column(
        DECIMAL, default=1.0
    )  # если коофициент ниже 1.0 то кооф будет понижать

    rarity_id: Mapped[str] = mapped_column(ForeignKey("rarity_category.ext_id"))
    rarity_category: Mapped["RarityCategory"] = relationship(
        "RarityCategory", back_populates="item"
    )

    compound = relationship("ItemCompound", back_populates="item")
    cases = relationship("Case", secondary=case_items, back_populates="items")
    user_items: Mapped[List["UserItems"]] = relationship(
        "UserItems", back_populates="user_items"
    )


class Test(Base):
    __tablename__ = "test"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    test = Column(String)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, unique=True, default=generator_id)
    username = Column(String, unique=True, nullable=True)
    email = Column(String, unique=True)
    password_hash = Column(String)
    image = Column(String)
    balance = Column(Integer, default=0)
    locale = Column(String, default="ru")
    auth_date = Column(DateTime, default=datetime.utcnow)
    verified = Column(Boolean, default=False)
    active = Column(Boolean, default=True)
    opened_cases = relationship(
        "Case", secondary=case_openings, back_populates="user_opened"
    )
    inventory_items: Mapped[List["UserItems"]] = relationship(
        "UserItems", back_populates="user"
    )
    social_accounts = relationship("SocialAuth", back_populates="user")
    tokens = relationship("UserToken", back_populates="user")
    individual_percent = Column(DECIMAL, default=1.0)

    async def update(self, data: dict):
        async with get_session() as session:
            for key in data.keys():
                if not hasattr(self, key):
                    raise AttributeError(f"Have no key {key}")
                else:
                    setattr(self, key, data[key])
            await session.commit()


class UserItems(Base):
    __tablename__ = "users_items"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    count: int = Column(Integer, nullable=False, default=1)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="user_items")
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))
    item: Mapped["Item"] = relationship("Item", back_populates="item")


class SocialAuth(Base):
    __tablename__ = "social_auths"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    provider = Column(String)
    social_id = Column(Integer, unique=True)
    user = relationship("User", back_populates="social_accounts")


class Deposit(Base):
    __tablename__ = "deposits"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    amount = Column(DECIMAL)
    deposited_on = Column(DateTime, default=datetime.utcnow)


class Expenditure(Base):
    __tablename__ = "expenditures"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    amount = Column(DECIMAL)
    case_id = Column(String, ForeignKey("cases.case_id"))
    spent_on = Column(DateTime, default=datetime.utcnow)


class UserToken(Base):
    __tablename__ = "users_tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    token = Column(String, unique=True)
    date_created = Column(DateTime, default=datetime.utcnow)
    date_expired = Column(DateTime)
    user = relationship("User", back_populates="tokens")


class ItemsFindingsStatus(Base):
    __tablename__ = "items_findings_status"

    id = Column(Integer, primary_key=True, autoincrement=True)
    status_id = Column(String, default=generator_id)
    name = Column(String)
    ext_id = Column(String, unique=True)


class ItemsFindings(Base):
    __tablename__ = "items_findings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    itemfs_id = Column(String, unique=True, default=generator_id)
    user_id = Column(String, ForeignKey("users.user_id"))
    item_id = Column(String, ForeignKey("items.item_id"))
    genshin_user_id = Column(String)
    status = Column(String, ForeignKey("items_findings_status.ext_id"))
    active = Column(Boolean, default=True)
    moogoald_order_id = Column(String)
    total = Column(DECIMAL)
    created_at = Column(DateTime, default=datetime.utcnow)


class OrderMoogold(Base):
    __tablename__ = "order_moogold"
    id = Column(Integer, primary_key=True, autoincrement=True)
    itemfs_id = Column(String, ForeignKey("items_findings.itemfs_id"))
    order_id = Column(String)


# from sqlalchemy import Table, ForeignKey, Column, Integer, String, Boolean, DateTime, DECIMAL
# from sqlalchemy.orm import relationship
# from database import Base
# from datetime import datetime
# from utils import generator_id

# role_permissions = Table('role_permissions', Base.metadata,
#     Column('role_id', String, ForeignKey('roles.role_id'), primary_key=True),
#     Column('permission_id', String, ForeignKey('permissions.permission_id'), primary_key=True)
# )

# admin_roles = Table('admin_roles', Base.metadata,
#     Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
#     Column('admin_id', Integer, ForeignKey('administrators.id'), primary_key=True)
# )


# class Role(Base):
#     __tablename__ = "roles"

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     role_id = Column(String, unique=True, default=generator_id)
#     name = Column(String, unique=True)
#     permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")
#     administrators = relationship("Administrator", secondary=admin_roles, back_populates="roles")

# class Permission(Base):
#     __tablename__ = "permissions"

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     permission_id = Column(String, unique=True, default=generator_id)
#     name = Column(String)
#     roles = relationship("Role", secondary=role_permissions, back_populates="permissions")

# class Administrator(Base):
#     __tablename__ = "administrators"

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     admin_id = Column(String, unique=True, default=generator_id)
#     username = Column(String, unique=True)
#     first_name = Column(String)
#     last_name = Column(String)
#     email = Column(String, unique=True)
#     password_hash = Column(String)
#     image = Column(String)
#     date_created = Column(DateTime, default=datetime.utcnow)
#     is_active = Column(Boolean, default=True)
#     last_login = Column(DateTime)
#     roles = relationship("Role", secondary=admin_roles, back_populates="administrators")


# class Category(Base):
#     __tablename__ = "categories"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     category_id = Column(String, unique=True, default=generator_id)
#     name = Column(String)
#     cases = relationship('Case', back_populates='category', lazy='dynamic')

# class Case(Base):
#     __tablename__ = "cases"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     case_id = Column(String, unique=True, default=generator_id)
#     name = Column(String)
#     image = Column(String)
#     cost = Column(Integer)
#     category_id = Column(Integer, ForeignKey('categories.id'))
#     category = relationship('Category', back_populates='cases')
#     items = relationship('Item', back_populates='case', lazy='dynamic')


# user_inventory = Table('user_inventory', Base.metadata,
#     Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
#     Column('item_id', Integer, ForeignKey('items.id'), primary_key=True),
#     Column('acquired_date', DateTime, default=datetime.utcnow)
# )

# class Item(Base):
#     __tablename__ = "items"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     item_id = Column(String, unique=True, default=generator_id)
#     name = Column(String)
#     image = Column(String)
#     case_id = Column(Integer, ForeignKey('cases.id'))
#     case = relationship('Case', back_populates='items')
#     user_items = relationship("User", secondary=user_inventory, back_populates="inventory_items")

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     user_id = Column(String, unique=True, default=generator_id)
#     username = Column(String, unique=True, nullable=True)
#     email = Column(String, unique=True)
#     password_hash = Column(String)
#     image = Column(String)
#     balance = Column(Integer, default=0)
#     locale = Column(String, default="ru")
#     auth_date = Column(DateTime, default=datetime.utcnow)
#     verified = Column(Boolean, default=False)
#     active = Column(Boolean, default=True)
#     inventory_items = relationship("Item", secondary=user_inventory, back_populates="user_items")

#     social_accounts = relationship("SocialAuth", back_populates="user")
#     tokens = relationship("UserToken", back_populates="user")

# class Deposit(Base):
#     __tablename__ = "deposits"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     amount = Column(DECIMAL)  # или DECIMAL, если нужна точность
#     deposited_on = Column(DateTime, default=datetime.utcnow)

# class Expenditure(Base):
#     __tablename__ = "expenditures"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     amount = Column(DECIMAL)
#     case_id = Column(Integer, ForeignKey('cases.id'))  # для отслеживания, на что потрачены средства
#     spent_on = Column(DateTime, default=datetime.utcnow)


# class SocialAuth(Base):
#     __tablename__ = "social_auths"

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     provider = Column(String)
#     social_id = Column(Integer, unique=True)

#     user = relationship("User", back_populates="social_accounts")


# class UserToken(Base):
#     __tablename__ = "users_tokens"

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     token = Column(String, unique=True)
#     date_created = Column(DateTime, default=datetime.utcnow)
#     date_expired = Column(DateTime)
#     user = relationship("User", back_populates="tokens")
