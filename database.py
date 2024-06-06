from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import create_engine

from config import settings


engine_sync = create_engine(
    url=settings.database_url_psycopg,
    echo=True,
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
