from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from database import get_async_session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """Асинхронная функция получения пользователя.
    Depends - функция FastApi и она отвечает за инъекцию зависимостей(
    использование в нащих функциях внешних функций)."""
    yield SQLAlchemyUserDatabase(session, User)
