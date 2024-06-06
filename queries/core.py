from sqlalchemy import text

from models import metadata
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
        result = await conn.execute(text("SELECT 1,2,3 union select 4,5,6"))
        print(result)
        # <sqlalchemy.engine.cursor.CursorResult object at 0x0000022730E49C50> - итератор алхимии
        print(f"{result.first()}")


def create_tables():
    metadata.create_all(engine_sync)