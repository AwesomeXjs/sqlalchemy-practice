from enum import Enum
from typing import Annotated
from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import (
    func,
    text,
    Table,
    Index,
    Column,
    String,
    Integer,
    MetaData,
    ForeignKey,
    CheckConstraint,
)

from database import Base, str256

# ИМПЕРАТИВНЫЙ ПОДХОД К ПОСТРОЕНИЮ МОДЕЛИ:
metadata = MetaData()


workers_table = Table(
    "workers",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String),
)

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

    resumes: Mapped[list["ResumesOrm"]] = relationship(
        back_populates="worker",
        # backref="worker",  # backref - неявное указание на другой relationship (не рекомендуется)
    )

    # Если у нас связь one2many и мы не хотим подгружать очень много лишних данных для одного пользователя то мы можем создать отдельный relationship с нужным фильтром
    resumes_parttime: Mapped[list["ResumesOrm"]] = relationship(
        back_populates="worker",
        # backref="worker",  # backref - неявное указание на другой relationship (не рекомендуется)
        primaryjoin="and_(WorkersOrm.id == ResumesOrm.worker_id, ResumesOrm.workload == 'parttime')",
        order_by="ResumesOrm.id.desc()",
        # lazy="selectin",  # атрибут lazy будет неявно указывать каким способом нужно подгружать данные
    )


class ResumesOrm(Base):
    __tablename__ = "resumes"

    id: Mapped[intpk]
    title: Mapped[str256]
    compensation: Mapped[int | None]
    workload: Mapped[Workload]
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    worker: Mapped["WorkersOrm"] = relationship(back_populates="resumes")

    __table_args__ = (
        Index(
            "title_index",
            "title",
        ),
        CheckConstraint("compensation > 0", name="check_compensation_positive"),
    )
