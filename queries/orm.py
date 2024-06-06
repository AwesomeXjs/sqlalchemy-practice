from database import engine_sync, Base, async_session_factory
from models import WorkersOrm, ResumesOrm


def create_tables():
    # engine_sync.echo = False
    Base.metadata.drop_all(engine_sync)
    Base.metadata.create_all(engine_sync)


# insert (добавление) через орм.
def insert_data(session_factory, first_username: str, second_username: str):
    with session_factory() as session:
        worker_bobr = WorkersOrm(username=first_username)
        worker_volk = WorkersOrm(username=second_username)
        session.add_all([worker_bobr, worker_volk])
        session.commit()


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
