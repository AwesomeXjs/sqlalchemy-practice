from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from config import settings


class Base(DeclarativeBase):
    pass


# ENGINE нужен чтобы коннектится к нашей бд и делать какие то запросы
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


# SESSION:
# Session - сессия нужна для транзакций в бд.
# Когда мы входим в сессию мы открываем транзакцию, делаем набор каких то действий и закрываем транзакцию вызывая коммит.
# После коммита данные либо попадают в бд либо нет.

# Sessionmaker (фабрика сессий) - нужен чтобы один раз сконфигурировать наши сессии и потом просто использовать фабрику,
# а не таскать engine по модулям и не задавать каждый раз одни и теже параметры

sync_session_factory = sessionmaker(engine_sync)
async_session_factory = async_sessionmaker(engine_async)
