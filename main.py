import asyncio

from database import Base
from queries import SyncCore, AsyncCore, SyncORM, AsyncORM
from database import sync_session_factory, engine_sync, async_session_factory
from models import (
    Base,
    metadata,
    Workload,
    ResumesOrm,
    WorkersOrm,
    VacansiesOrm,
    workers_table,
)

SyncORM.create_tables(engine_sync=engine_sync, Base=Base)
SyncORM.insert_workers(
    session_factory=sync_session_factory,
    WorkersOrm=WorkersOrm,
    first_username="Dima",
    second_username="Vlad",
)
SyncORM.insert_workers(
    session_factory=sync_session_factory,
    WorkersOrm=WorkersOrm,
    first_username="Petya",
    second_username="Volodya",
)
SyncORM.insert_resumes(
    sync_session_factory=sync_session_factory,
    model=ResumesOrm,
    compensation=150000,
    title="JavaScript",
    worker_id=3,
    workload=Workload.fulltime,
)
SyncORM.insert_resumes(
    sync_session_factory=sync_session_factory,
    model=ResumesOrm,
    compensation=150000,
    title="Python Java",
    worker_id=1,
    workload=Workload.fulltime,
)
SyncORM.insert_resumes(
    sync_session_factory=sync_session_factory,
    model=ResumesOrm,
    compensation=150000,
    title="C#",
    worker_id=1,
    workload=Workload.fulltime,
)
SyncORM.insert_resumes(
    sync_session_factory=sync_session_factory,
    model=ResumesOrm,
    compensation=150000,
    title="Java",
    worker_id=4,
    workload=Workload.fulltime,
)
SyncORM.add_vacancies(
    session=sync_session_factory, resume_table=ResumesOrm, vacancy_table=VacansiesOrm
)
SyncORM.select_resumes_with_all_relationships(
    session=sync_session_factory, resume_table=ResumesOrm, vacancy_table=VacansiesOrm
)
