import enum
from datetime import date, datetime

from sqlalchemy import (TIMESTAMP, CheckConstraint, Enum, Numeric, ForeignKey, String,
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

        ADMIN = 'admin'
        EMPLOYEE = 'employee'
        STAFF = 'staff'

    __table_args__ = (
        CheckConstraint('date_of_birth < {}'.format(func.current_timestamp())),
    )

    first_name: Mapped[str] = mapped_column(String(length=150))
    last_name: Mapped[str] = mapped_column(String(length=150))
    username: Mapped[str] = mapped_column(String(length=150), unique=True)
    password: Mapped[str] = mapped_column(String(length=100))
    date_of_birth: Mapped[date]
    status: Mapped[Status] = mapped_column(
        Enum(
            Status,
            name='user_status',
            values_callable=lambda obj: [e.value for e in obj],
        ), server_default=Status.EMPLOYEE.value
    )
    is_blocked: Mapped[bool] = mapped_column(default=True)
    department_id: Mapped[int] = mapped_column(
        ForeignKey('department.id', ondelete='SET NULL'), nullable=True
    )
    department: Mapped['Department'] = relationship(back_populates='employees')
    position_id: Mapped[int] = mapped_column(
        ForeignKey('position.id', ondelete='SET NULL'), nullable=True
    )
    position: Mapped['Position'] = relationship(back_populates='employees')
    salary_id: Mapped[int] = mapped_column(
        ForeignKey('salary.id', ondelete='SET NULL'), nullable=True
    )
    salary: Mapped['Salary'] = relationship(back_populates='employee')


class Salary(Base):
    """Модель для заработной платы."""

    __table_args__ = (
        CheckConstraint('raise_date >= {}'.format(func.current_timestamp())),
    )

    amount: Mapped[float] = mapped_column(Numeric(9,2), CheckConstraint('amount > 0'))
    raise_date: Mapped[date]
    employee: Mapped['User'] = relationship(back_populates='salary')


class Department(Base):

    title: Mapped[str] = mapped_column(String(length=256), unique=True)
    employees: Mapped[list['User']] = relationship(back_populates='department')


class Position(Base):

    title: Mapped[str] = mapped_column(String(length=100), unique=True)
    employees: Mapped[list['User']] = relationship(back_populates='position')
