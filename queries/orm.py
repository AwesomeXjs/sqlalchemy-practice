from sqlalchemy import select, insert

from models import WorkersOrm, ResumesOrm
from database import async_session_factory, Base, engine_sync, sync_session_factory


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

            # Вариант для добавления всех нужных элементов:
            worker_bobr = WorkersOrm(username=first_username)
            worker_volk = WorkersOrm(username=second_username)
            session.add_all([worker_bobr, worker_volk])

            # Вариант для добавления одного элемента:
            # stmt = insert(table=WorkersOrm).values(username="Dima")
            # session.execute(stmt)
            session.commit()

    # SELECT
    @staticmethod
    def select_workers(id: int = 1):
        with sync_session_factory() as session:
            # worker = session.get(WorkersOrm, id) - получаем одного работника
            query = select(WorkersOrm)
            result = session.execute(query)
            # workers = (
            #     result.all()
            # )  # sqlalchemy возвращает список из кортежей моделей воркеров (создает экземпляры наших моделей)

            workers = (
                result.scalars().all()
            )  # scalars возвращает первое значение каждого кортежа
            print([el.username for el in workers])

    # UPDATE
    @staticmethod
    def update_worker(worker_id: int = 2, new_username: str = "Misha"):
        with sync_session_factory() as session:
            worker = session.get(WorkersOrm, worker_id)  # - получаем одного работника
            worker.username = new_username
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
