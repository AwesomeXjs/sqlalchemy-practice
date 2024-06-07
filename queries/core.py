import queries
from sqlalchemy import MetaData, insert, select, text, update

from models import workers_table
from database import engine_sync, engine_async


def get_123_sync():
    with engine_sync.connect() as conn:  # engine.begin() - делает комит в конце всегда при выходе из контекстного менеджера,
        # engine.connect() делает rollback при выходе из контекстного менеджера
        result = conn.execute(text("SELECT 1,2,3 union select 4,5,6"))
        # чтобы извлечь ответ из итератора алхимии мы должны как то по нему пройтись
        print(f"VERSION: {result.first()}")  # VERSION: (1, 2, 3)
        # при попытке извлечь один элемент из таблицы мы получаем кортеж
        conn.commit()


# Асинхронный вариант
async def get_123_async():
    async with engine_async.connect() as conn:
        stmt = "SELECT 1,2,3 union select 4,5,6"
        result = await conn.execute(text(stmt))
        print(result)
        # <sqlalchemy.engine.cursor.CursorResult object at 0x0000022730E49C50> - итератор алхимии
        print(f"{result.first()}")


class SyncCore:
    @staticmethod
    def create_tables(metadata):
        metadata.drop_all(engine_sync)
        metadata.create_all(engine_sync)

    @staticmethod
    def insert_data(workers_table):
        with engine_sync.connect() as conn:
            # stmt - insert / update/ delete
            # сырой запрос:
            # stmt = """INSERT INTO workers (username) VALUES
            #         ('Bobr'),
            #         ('Volk');"""

            # query builder:
            stmt = insert(workers_table).values(
                [
                    {"username": "another volk"},
                    {"username": "another bobr"},
                ]
            )
            conn.execute(stmt)
            conn.commit()

    # SELECT
    @staticmethod
    def select_workers(workers_table, var: str = "all"):
        with engine_sync.connect() as conn:
            query = select(workers_table)  # SELECT * FROM workers_table
            result = conn.execute(query)  # sqlalchemy возвращает итератор
            if var == "one":
                workers = result.first()
            if var == "all":
                workers = result.all()
            print(workers)

    # UPDATE
    @staticmethod
    def update_worker(worker_id: int = 2, new_username: str = "Misha"):
        with engine_sync.connect() as conn:
            # СЫРОЙ UPDATE запрос:
            # stmt = text(
            #     "UPDATE workers SET username=:username WHERE id=:worker_id"
            # )  # сырой запрос
            # stmt = stmt.bindparams(username=new_username, worker_id=worker_id)
            stmt = (
                update(workers_table).values(username=new_username)
                # .where(workers_table.id == worker_id)
                .filter_by(id=worker_id)
            )
            conn.execute(stmt)
            conn.commit()


class AsyncCore:
    @staticmethod
    async def create_tables(metadata: MetaData):
        async with engine_async.begin() as conn:
            await conn.run_sync(metadata.drop_all)
            await conn.run_sync(metadata.create_all)

    @staticmethod
    async def insert_workers(workers_table):
        async with engine_async.connect() as conn:
            stmt = insert(workers_table).values(
                [
                    {"username": "Jack"},
                    {"username": "Michael"},
                ]
            )
            await conn.execute(stmt)
            await conn.commit()
