from datetime import datetime
from typing import AsyncGenerator

from fastapi import Depends
# from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
# from sqlalchemy import Column, String, Boolean, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker #, Mapped, mapped_column

from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS
# from src.auth.models import role


#По умолчанию здесь стоит sqlite. Изменим на нашу БД Postresql с секретами из config.
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
#Аналог metadata в моделях.
Base: DeclarativeMeta = declarative_base()

#engine(движок) - точка входа sqlalchemy в наше приложение. использует ссылку на базу данных
engine = create_async_engine(DATABASE_URL)
#engine создаем временные соединения, чтобы можно было работать с БД.(CRUD)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Функцию create_all нужно избегать.
# async def create_db_and_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Функцию получения асинхронной сессии."""
    async with async_session_maker() as session:
        yield session