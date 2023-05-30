import enum
from datetime import date, datetime

from sqlalchemy import TIMESTAMP, Enum, ForeignKey, String, func
from sqlalchemy.ext.declarative import as_declarative, declared_attr  # noqa
from sqlalchemy.orm import Mapped, mapped_column, relationship


@as_declarative()
class Base:
    """Базовая модель."""

    @declared_attr
    def __tablename__(cls): # noqa
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(),
        server_default=func.current_timestamp(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(),
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )


class User(Base):
    """Модель для пользователя."""

    class Status(enum.Enum):
        """Статус пользователя."""

        BLOCKED = 'blocked'
        VERIFIED = 'verified'
        ADMIN = 'admin'
        SELLER = 'seller'

    first_name: Mapped[str] = mapped_column(String(length=150))
    last_name: Mapped[str] = mapped_column(String(length=150))
    nick_name: Mapped[str] = mapped_column(String(length=150), unique=True)
    password: Mapped[str] = mapped_column(String(length=100))
    date_birth: Mapped[date]
    status: Mapped[Status] = mapped_column(
        Enum(
            Status,
            name='user_status',
            values_callable=lambda obj: [e.value for e in obj],
        ), default=Status.BLOCKED.value
    )
    phone: Mapped[str] = mapped_column(String(length=20), unique=True)
    address_id: Mapped[int] = mapped_column(
        ForeignKey('address.id', ondelete='SET NULL')
    )
    address: Mapped['Address'] = relationship(back_populates='clients')
    permission_id: Mapped[int] = mapped_column(
        ForeignKey('permission.id', ondelete='SET DEFAULT'), server_default=''
    )  # declare the default value!!!!!
    right_level: Mapped['Permission'] = relationship(back_populates='users')


class Product(Base):
    """Модель для продукта."""

    title: Mapped[str] = mapped_column(String(length=256))
    description: Mapped[str]


class Category(Base):
    """Модель для категорий продуктов."""

    name: Mapped[str] = mapped_column(String(length=120))
    permission_id: Mapped[int] = mapped_column(
        ForeignKey('permission.id', ondelete='CASCADE')
    )
    right_level: Mapped['Permission'] = relationship(
        back_populates='categories'
    )


class Permission(Base):
    pass


class Address(Base):
    pass
