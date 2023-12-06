from datetime import datetime

from sqlalchemy import (MetaData, Table, Column, JSON,
                         Integer, String, TIMESTAMP, ForeignKey)

# Создаем переменную metadata и потом когда будем создавать таблицы, будем ее изменять.
metadata = MetaData()

# Далее создадим таблицу roles, со столбцами
roles = Table(
    "roles",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON),
)

# Далее сделаем таблицу с юзерами
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("password", String, nullable=False),
    Column("registred_at", TIMESTAMP, default=datetime.utcnow),
    Column("role_id", Integer, ForeignKey("roles.id")),
)


