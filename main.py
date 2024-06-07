import asyncio

from database import Base
from database import sync_session_factory, engine_sync
from queries import SyncCore, AsyncCore, SyncORM, AsyncORM
from models import WorkersOrm, Workload, workers_table, metadata, Base, ResumesOrm

# SyncCore.create_tables(metadata)
# insert_data(
#     session_factory=sync_session_factory, first_username="Bobr", second_username="Volk"
# )
# asyncio.run(async_insert_data())
# asyncio.run(get_worker_by_id(1))


# SyncCore.insert_data(workers_table=workers_table)
# SyncCore.select_workers(workers_table)
# SyncCore.update_worker(new_username="Dima")

SyncORM.create_tables(engine_sync=engine_sync, Base=Base)
SyncORM.insert_workers(
    session_factory=sync_session_factory,
    first_username="Dima",
    second_username="Yo",
    WorkersOrm=WorkersOrm,
)
# SyncORM.select_workers()
SyncORM.update_worker(
    new_username="Oleg",
    worker_id=1,
    WorkersOrm=WorkersOrm,
    sync_session_factory=sync_session_factory,
)

resumes = [
    {
        "title": "Python Developer",
        "workload": Workload.parttime,
        "compensation": 100000,
    },
    {
        "title": "Java Script Developer",
        "workload": Workload.fulltime,
        "compensation": 160000,
    },
    {
        "title": "Python Developer",
        "workload": Workload.fulltime,
        "compensation": 130000,
    },
]


for el in resumes:
    SyncORM.insert_resumes(
        compensation=el.get("compensation"),
        title=el.get("title"),
        workload=el.get("workload"),
        table=ResumesOrm,
        sync_session_factory=sync_session_factory,
        worker_id=2,
    )

SyncORM.select_resumes_avg_compensation(
    table=ResumesOrm, sync_session_factory=sync_session_factory
)
