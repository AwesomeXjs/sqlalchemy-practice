from datetime import datetime
from enum import Enum

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, func, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from database import Base

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


class Workload(Enum):
    parttime = "parttime"
    fulltime = "fulltime"


# ДЕКЛАРАТИВНЫЙ ПОДХОД
# DeclarativeBase - главный класс который будет управляет нашими таблицами. Содержит метадату
class WorkersOrm(Base):
    __tablename__ = "workers"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]


class ResumesOrm(Base):
    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    compensation: Mapped[int | None]
    workload: Mapped[Workload]
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        default=datetime.utcnow,
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
