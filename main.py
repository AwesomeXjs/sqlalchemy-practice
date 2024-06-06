import asyncio

from queries import create_tables, insert_data, async_insert_data
from database import Base
from database import sync_session_factory

create_tables()
insert_data(
    session_factory=sync_session_factory, first_username="Bobr", second_username="Volk"
)
asyncio.run(async_insert_data())
