from datetime import datetime

from sqlalchemy import (Boolean, MetaData, Table, Column, JSON,
                         Integer, String, TIMESTAMP, ForeignKey)

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

# Далее сделаем таблицу с юзерами
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