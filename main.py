import asyncio

from database import Base
from database import sync_session_factory
from queries import create_tables, insert_data, async_insert_data, get_worker_by_id

# create_tables()
# insert_data(
#     session_factory=sync_session_factory, first_username="Bobr", second_username="Volk"
# )
# asyncio.run(async_insert_data())
# asyncio.run(get_worker_by_id(1))
