from fastapi import FastAPI

from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate
# from auth.models import User
# from operations.router import router as router_operation

# Далее создаем приложение, которое явл-ся экземпляром FastAPI,  зададим ему понятное имя
app = FastAPI(
    title="Traiding App"
)

#Добавим роутер для авторизации 
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

#Роутер для создания и считывания пользователя
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)


# app.include_router(router_operation)