import asyncio

from database import Base
from queries import SyncCore, AsyncCore, SyncORM, AsyncORM
from database import sync_session_factory, engine_sync, async_session_factory
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

# SyncORM.create_tables(engine_sync=engine_sync, Base=Base)
# SyncORM.insert_workers(
#     session_factory=sync_session_factory,
#     first_username="Dima",
#     second_username="Yo",
#     WorkersOrm=WorkersOrm,
# )
# # SyncORM.select_workers()
# SyncORM.update_worker(
#     new_username="Oleg",
#     worker_id=1,
#     WorkersOrm=WorkersOrm,
#     sync_session_factory=sync_session_factory,
# )
# workers = [
#     {"username": "Yan"},
#     {"username": "Alex"},
#     {"username": "Chris"},
# ]


resumes = [
    {
        "title": "Python Developer",
        "workload": Workload.parttime,
        "compensation": 100000,
        "worker_id": 1,
    },
    {
        "title": "Java Script Developer",
        "workload": Workload.fulltime,
        "compensation": 160000,
        "worker_id": 2,
    },
    {
        "title": "Python Developer",
        "workload": Workload.parttime,
        "compensation": 170000,
        "worker_id": 3,
    },
    {
        "title": "C++ Developer",
        "workload": Workload.fulltime,
        "compensation": 120000,
        "worker_id": 2,
    },
    {
        "title": "C# Developer",
        "workload": Workload.parttime,
        "compensation": 190000,
        "worker_id": 1,
    },
    {
        "title": "Go Developer",
        "workload": Workload.fulltime,
        "compensation": 5000,
        "worker_id": 3,
    },
]


# for el in resumes:
#     SyncORM.insert_resumes(
#         compensation=el.get("compensation"),
#         title=el.get("title"),
#         workload=el.get("workload"),
#         model=ResumesOrm,
#         sync_session_factory=sync_session_factory,
#         worker_id=el.get("worker_id"),
#     )

# SyncORM.select_resumes_avg_compensation(
#     table=ResumesOrm, sync_session_factory=sync_session_factory
# )

# asyncio.run(
#     AsyncORM.insert_additional_resumes(
#         sync_session_factory=async_session_factory,
#         table_resumes=ResumesOrm,
#         table_workers=WorkersOrm,
#         workers=workers,
#         resumes=resumes,
#     )
# )

# asyncio.run(AsyncORM.join_cte_subquery_window_func(session=async_session_factory))

# SyncORM.select_workers_with_join_relationship(
#     session=sync_session_factory, worker_model=WorkersOrm
# )
SyncORM.select_in_workers_with_join_relationship(
    session=sync_session_factory, worker_model=WorkersOrm
)
