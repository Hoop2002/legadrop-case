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
    Time,
    select,
)
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates, joinedload

from database import Base, get_session
from utils import generator_id, default_case_name


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


case_conditions = Table(
    "case_conditions",
    Base.metadata,
    Column("condition_id", String, ForeignKey("conditions.condition_id")),
    Column("case_id", String, ForeignKey("cases.case_id")),
)


class Conditions(Base):
    __tablename__ = "conditions"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    condition_id: str = Column(String, unique=True, default=generator_id)
    type_condition: str = Column(
        PgEnum("calcs", "time", name="condition_types"),
        nullable=False,
        default="calcs",
        server_default="calcs",
    )
    price: float = Column(
        DECIMAL, default=0, nullable=False
    )  # сумма, которую нужно внести
    time: datetime.time = Column(Time)  # Время в течении которого нужно внести сумму
    timer_reboot: datetime.time = Column(
        Time
    )  # время через которое опять можно открыть кейс

    cases: Mapped["Case"] = relationship(
        "Case", secondary=case_conditions, back_populates="conditions"
    )


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(String, unique=True, default=generator_id)
    name = Column(String)
    cases = relationship("Case", back_populates="category", lazy="dynamic")


class Case(Base):
    __tablename__ = "cases"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    case_id: str = Column(String, unique=True, default=generator_id)
    name: str = Column(String, unique=True, nullable=False)
    translit_name: str = Column(
        String,
        default=default_case_name,
        onupdate=default_case_name,
        nullable=False,
        unique=True,
    )
    image = Column(String)
    price: float = Column(DECIMAL, nullable=False, default=0)
    case_free: bool = Column(
        Boolean, default=False, nullable=False, server_default=str(False)
    )
    category_id: str = Column(String, ForeignKey("categories.category_id"))
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

    category = relationship("Category", back_populates="cases")
    items = relationship("Item", secondary=case_items, back_populates="cases")
    user_opened = relationship(
        "User", secondary=case_openings, back_populates="opened_cases"
    )
    conditions: Mapped["Conditions"] = relationship(
        "Conditions", secondary=case_conditions, back_populates="cases"
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
        "UserItems", back_populates="item"
    )


class Test(Base):
    __tablename__ = "test"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    test = Column(String)


used_promo = Table(
    "used_promo",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("promo_id", Integer, ForeignKey("promo_codes.id"), primary_key=True),
    Column("used_date", DateTime, default=datetime.utcnow, nullable=False),
)


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
    individual_percent = Column(DECIMAL, default=1.0)

    opened_cases = relationship(
        "Case", secondary=case_openings, back_populates="user_opened"
    )
    user_items: Mapped[List["UserItems"]] = relationship(
        "UserItems", back_populates="user"
    )
    social_accounts = relationship("SocialAuth", back_populates="user")
    tokens = relationship("UserToken", back_populates="user")
    calcs: Mapped[List["Calc"]] = relationship(back_populates="user")
    promo_codes: Mapped[List["PromoCode"]] = relationship(
        secondary=used_promo, back_populates="users"
    )

    async def update(self, data: dict):
        async with get_session() as session:
            stmt = select(User).filter_by(id=self.id)
            user = await session.execute(stmt)
            user = user.scalar()
            for key in data.keys():
                if not hasattr(user, key):
                    raise AttributeError(f"Have no key {key}")
                else:
                    setattr(user, key, data[key])
            await session.commit()
            session.refresh(user)
            return user


class UserItems(Base):
    __tablename__ = "user_items"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    active: bool = Column(Boolean, default=True, nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="user_items")
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))
    item: Mapped["Item"] = relationship("Item", back_populates="user_items")

    # todo решить надо ли это
    # @property
    # def count(self) -> int:
    #     from database.database import SessionLocalSync
    #     from sqlalchemy import func
    #     try:
    #         session = SessionLocalSync()
    #         with session:
    #             stmt = select(func.count(UserItems.id)).filter_by(user_id=self.user_id, item_id=self.item_id)
    #             result = session.execute(stmt)
    #             return result.scalar()
    #     except Exception as err:
    #         print(err)
    #     finally:
    #         session.close()

    async def update(self, data: dict):
        async with get_session() as session:
            stmt = select(UserItems).filter_by(id=self.id)
            instance = await session.execute(stmt)
            instance = instance.scalar()
            for key in data.keys():
                if not hasattr(instance, key):
                    raise AttributeError(f"Have no key {key}")
                else:
                    setattr(instance, key, data[key])
            await session.commit()
            session.refresh(instance)
            return instance

    @classmethod
    async def create(cls, **kwargs) -> "UserItems":
        instance = cls(**kwargs)
        async with get_session() as session:
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
        return instance


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


class PromoCode(Base):
    __tablename__ = "promo_codes"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    promo_id: str = Column(String, unique=True, default=generator_id)
    name: str = Column(String, nullable=False)
    type_code: str = Column(
        PgEnum("bonus", "balance", name="promo_types"), nullable=False
    )
    summ: float = Column(DECIMAL, nullable=False, default=1)
    limit_activations: int = Column(Integer)
    to_date: datetime = Column(DateTime)

    activations: int = Column(Integer, default=0, nullable=False)
    active: bool = Column(Boolean, default=True)
    creation_date: datetime = Column(DateTime, default=datetime.utcnow())
    code_data: str = Column(String, unique=True, nullable=False, default=generator_id)

    calc: Mapped[List["Calc"]] = relationship(back_populates="promo_code")
    users: Mapped[List["User"]] = relationship(
        secondary=used_promo, back_populates="promo_codes"
    )

    async def activate_pomo(self, user_id):
        async with get_session() as session:
            stmt = select(User).where(User.user_id == user_id)
            result = await session.execute(stmt)
            user = result.scalar()
            stmt = (
                select(PromoCode)
                .filter_by(id=self.id)
                .options(joinedload(PromoCode.users))
            )
            result = await session.execute(stmt)
            instance: PromoCode = result.scalar()

            if self.type_code == "balance":
                calc = Calc(user=user, promo_code=instance, summ=instance.summ)
                session.add(calc)
                user.balance = user.balance + self.summ

            instance.users.append(user)
            instance.activations += 1
            if instance.limit_activations and (
                instance.activations >= instance.limit_activations
            ):
                instance.active = False
            await session.commit()
            return user

    @classmethod
    async def create(cls, **kwargs) -> "PromoCode":
        instance = cls(**kwargs)
        async with get_session() as session:
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
        return instance


class Calc(Base):
    __tablename__ = "calcs"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    calc_id: str = Column(String, unique=True, default=generator_id)
    summ: float = Column(DECIMAL, nullable=False)
    creation_date: datetime = Column(DateTime, default=datetime.utcnow, nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="calcs")
    promo_code_id: Mapped[int] = mapped_column(ForeignKey("promo_codes.id"))
    promo_code: Mapped["PromoCode"] = relationship(back_populates="calc")

    # calc_kind todo вид начисления, нужен ли, делать ли?
    # order todo тут связь с оплатой

    @validates("creation_date")
    def validate_creation_date(self, key, value):
        if self.creation_date:
            raise ValueError("Creation date cannot be modified.")


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
