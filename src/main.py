from datetime import datetime
from enum import Enum
from typing import Annotated, List, Optional, Union
from fastapi_users import fastapi_users, FastAPIUsers
from pydantic import BaseModel, Field

from fastapi import Depends, FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
# from fastapi.exceptions import ValidationError
from fastapi.exceptions import ValidationException
from fastapi.responses import JSONResponse

from auth.auth import auth_backend
from auth.database import User
from auth.schemas import UserRead, UserCreate
from auth.manager import get_user_manager

# Далее создаем приложение, которое явл-ся экземпляром FastAPI,  зададим ему понятное имя
app = FastAPI(
    title="Traiding App"
)

# Создаем инстанс fastapi_users
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

#Добавим роутер для авторизации 
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

#Роутер для создания и считывания пользователя
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user()

@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    """Защищенный эндпойнт."""
    return f"Hello, {user.username}"


@app.get("/unprotected-route")
def unprotected_route():
    """Незащищенный эндпойнт."""
    return f"Hello, anonym"


app.include_router(router_operation)