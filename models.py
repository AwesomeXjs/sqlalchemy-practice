from datetime import datetime
from enum import Enum
from typing import Annotated

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, func, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from database import Base, str256

# ИМПЕРАТИВНЫЙ ПОДХОД К ПОСТРОЕНИЮ МОДЕЛИ:
# metadata = MetaData()
#
#
# workers_table = Table(
#     "workers",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("username", String),
# )

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[
    datetime,
    mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        default=datetime.utcnow,
    ),
]
updated_at = Annotated[
    datetime,
    mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    ),
]


class Workload(Enum):
    parttime = "parttime"
    fulltime = "fulltime"


# ДЕКЛАРАТИВНЫЙ ПОДХОД
# DeclarativeBase - главный класс который будет управляет нашими таблицами. Содержит метадату
class WorkersOrm(Base):
    __tablename__ = "workers"
    id: Mapped[intpk]
    username: Mapped[str]


class ResumesOrm(Base):
    __tablename__ = "resumes"

    id: Mapped[intpk]
    title: Mapped[str256]
    compensation: Mapped[int | None]
    workload: Mapped[Workload]
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
