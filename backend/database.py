from sqlalchemy import event
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import AsyncGenerator

# Создаем асинхронный движок для SQLite
DATABASE_URL = "sqlite+aiosqlite:///database.db"
engine = create_async_engine(DATABASE_URL, echo=True)

# Настраиваем асинхронную сессию
async_session = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Создаем базовый класс для моделей
Base = declarative_base()

# Этот декоратор заставляет SQLAlchemy выполнять код при каждом новом подключении
@event.listens_for(engine.sync_engine, "connect")
def register_custom_functions(dbapi_connection, connection_record):
    # Регистрация функции 'py_lower', которая использует Python .lower(), поскольку методы для этого в SQLite не работают с кириллицей
    # 1 - количество аргументов
    dbapi_connection.create_function("py_lower", 1, lambda x: x.lower() if x else x)
    # Теперь в SQL будет доступна функция py_lower()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Зависимость для получения сессии базы данных.
    Используется в маршрутах FastAPI с Depends.
    """
    session = async_session()
    try:
        yield session
    finally:
        await session.close()

async def get_db_session() -> AsyncSession:
    """
    Функция для прямого получения сессии базы данных.
    Для использования в сервисах без Depends.
    """
    return async_session()