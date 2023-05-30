import enum
from datetime import date, datetime

from sqlalchemy import (TIMESTAMP, CheckConstraint, Enum, ForeignKey, String,
                        func)
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
        ACTIVE = 'active'
        ADMIN = 'admin'
        STUFF = 'stuff'

    __table_args__ = (
        CheckConstraint('date_birth < {}'.format(func.current_timestamp())),
    )

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
    department_id: Mapped[int] = mapped_column(
        ForeignKey('department.id', ondelete='SET NULL')
    )
    department: Mapped['Department'] = relationship(back_populates='employees')
    position_id: Mapped[int] = mapped_column(
        ForeignKey('position.id', ondelete='SET NULL')
    )
    position: Mapped['Position'] = relationship(back_populates='employees')
    permission_id: Mapped[int] = mapped_column(
        ForeignKey('permission.id', ondelete='SET DEFAULT'), server_default=''
    )  # declare the default value!!!!!
    right_level: Mapped['Permission'] = relationship(back_populates='users')


class Salary(Base):
    """Модель для заработной платы."""

    __table_args__ = (
        CheckConstraint('raise_date >= {}'.format(func.current_timestamp())),
    )

    amount: Mapped[int] = mapped_column(CheckConstraint('amount > 0'))
    raise_date: Mapped[date]


class Department(Base):
    pass


class Position(Base):
    pass


class Permission(Base):
    pass


class Address(Base):
    pass
