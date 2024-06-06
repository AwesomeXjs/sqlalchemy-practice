import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import URL, create_engine, text

from config import settings


engine_sync = create_engine(
    url=settings.database_url_psycopg,
    echo=False,
    pool_size=5,  # Максимум будет создано подключений при работае с алхимией
    max_overflow=10,  # максимум 10 доп подключений алхимия может еще создать если все 5 максимум подключений заполнено
)

engine_async = create_async_engine(
    url=settings.database_url_asyncpg,
    echo=False,
    pool_size=5,  # Максимум будет создано подключений при работае с алхимией
    max_overflow=10,  # максимум 10 доп подключений алхимия может еще создать если все 5 максимум подключений заполнено
)

# запросы в бд всегда делаются через контекстный менеджер

with engine_sync.connect() as conn:  # engine.begin() - делает комит в конце всегда при выходе из контекстного менеджера,
    # engine.connect() делает rollback при выходе из контекстного менеджера
    result = conn.execute(text("SELECT 1,2,3 union select 4,5,6"))
    # чтобы извлечь ответ из итератора алхимии мы должны как то по нему пройтись
    print(f"VERSION: {result.first()}")  # VERSION: (1, 2, 3)
    # при попытке извлечь один элемент из таблицы мы получаем кортеж
    conn.commit()


# Асинхронный вариант
async def get_123():
    async with engine_async.connect() as conn:
        result = await conn.execute(text("SELECT 1,2,3 union select 4,5,6"))
        print(result)
        # <sqlalchemy.engine.cursor.CursorResult object at 0x0000022730E49C50> - итератор алхимии
        print(f"{result.first()}")


asyncio.run(get_123())
