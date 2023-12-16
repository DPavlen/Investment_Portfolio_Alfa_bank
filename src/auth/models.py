from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import (Table, Column, Integer, String, TIMESTAMP, 
                        ForeignKey, JSON, Boolean, MetaData)
from database import Base

# from auth.models import role
# Создаем переменную metadata и потом когда будем создавать таблицы, будем ее изменять.
metadata = MetaData()

# Далее создадим таблицу roles, со столбцами
role = Table(
    "role",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON),
)

# Далее сделаем таблицу с юзерами - интеративный метод подхода.
user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow),
    Column("role_id", Integer, ForeignKey(role.c.id)),
    Column("hashed_password", String, nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),
)


#Изменяем тип UUID на ID в соответсвии с рекомендацией
class User(SQLAlchemyBaseUserTable[int], Base):
    """Декларативный метод подхода для SQLAlchemy.Рекомендует FastAPI_users
    Класс User. Наследуемся от базовой таблицы пользователей SQLAlchemy.
    Поля email, hashed_password, is_active, is_superuser, is_verified из SQLAlchemyBaseUserTable.
    Часть полей добавим из модели users."""
    #TO DO new field, example Mapped[str] = mapped_column(...)
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    role_id = Column(Integer, ForeignKey(role.c.id))
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)