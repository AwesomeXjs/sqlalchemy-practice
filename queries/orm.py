from sqlalchemy import select

from models import WorkersOrm, ResumesOrm
from database import engine_sync, Base, async_session_factory


class SyncORM:
    @staticmethod
    def create_tables():
        # engine_sync.echo = False
        Base.metadata.drop_all(engine_sync)
        Base.metadata.create_all(engine_sync)

    # insert (добавление) через орм.
    @staticmethod
    def insert_workers(
        session_factory,
        first_username: str,
        second_username: str,
    ):
        with session_factory() as session:
            worker_bobr = WorkersOrm(username=first_username)
            worker_volk = WorkersOrm(username=second_username)
            session.add_all([worker_bobr, worker_volk])
            session.commit()


class AsyncORM:
    @staticmethod
    async def async_insert_data():
        async with async_session_factory() as session:
            worker = WorkersOrm(username="New Worker from orm")
            session.add(worker)
            # resume = ResumesOrm(
            #     title="New resume",
            #     compensation=23,
            #     workload="parttime",
            #     worker_id=2,
            # )
            # session.add(resume)
            await session.commit()

    @staticmethod
    # Get запрос через орм
    async def get_worker_by_id(id: int):
        async with async_session_factory() as session:
            result = await session.get(WorkersOrm, id)
            print(result.username)
        # query = select(WorkersOrm).where(WorkersOrm.id == id)
        # result = await session.execute(query)
        # print(result.scalar())
