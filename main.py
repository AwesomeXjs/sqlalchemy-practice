import asyncio

from database import Base
from database import sync_session_factory
from models import workers_table, metadata
from queries import SyncCore, AsyncCore, SyncORM, AsyncORM

# SyncCore.create_tables(metadata)
# insert_data(
#     session_factory=sync_session_factory, first_username="Bobr", second_username="Volk"
# )
# asyncio.run(async_insert_data())
# asyncio.run(get_worker_by_id(1))


# SyncCore.insert_data(workers_table=workers_table)
# SyncCore.select_workers(workers_table)
# SyncCore.update_worker(new_username="Dima")

SyncORM.create_tables()
SyncORM.insert_workers(session_factory=sync_session_factory, first_username="Dima")
# SyncORM.select_workers()
# SyncORM.update_worker()
