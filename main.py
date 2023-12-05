from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
# from fastapi.exceptions import ValidationError
from fastapi.exceptions import ValidationException
from fastapi.responses import JSONResponse

# Далее создаем приложение, которое явл-ся экземпляром FastAPI,  зададим ему понятное имя
app = FastAPI(
    title="Traiding App"
)

# Благодаря этой функции клиент видит ошибки, происходящие на сервере, вместо 500 "Internal server error"
@app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )

# База данных пользователей. Соответсвенно у каждого есть id
fake_users = [
    {"id": 1, "role": "admin", "name": ["Bob"]},
    {"id": 2, "role": "investor", "name": "John"},
    {"id": 3, "role": "trader", "name": "Matt"},
    {"id": 4, "role": "investor", "name": "Homer", "degree": [
        {"id": 1, "created_at": "2020-01-01T00:00:00", "type_degree": "expert"}
    ]},
]

class DegreeType(Enum):
    """Валидация для квалификации типа степени трейдера (Degree Type)."""
    newbie = "newbie"
    expert = "expert"
    managing_director = "managing_director"


class Degree(BaseModel):
    """Модель Degree для модели User поля degree, где будет список экспертов."""
    id: int
    created_at: datetime
    type_degree: DegreeType


class User(BaseModel):
    """Модель списка юзеров.
    Добавим поле degree c отдельной описанной структурой данных Degree.
    Optional указывает, что атрибут degree может принимать значение None
    или тип данных, указанный после него список.
    """
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] = [ ]


# Далее создаем точку входа, для получения данных о пользователе # Оборачиваем в фигурные скобки {user_id} и далее в функции 
# get_user получаем параметр user_id и необходимо получить # конкретного пользователя с list_comprehesions
# Модель данных, которой мы отвечаем с помощью response_model
@app.get("/users/{user_id}", response_model=List[User])
def get_user(user_id: int):
    """Получаем по id текущего usera."""
    return [user for user in fake_users if user.get("id") == user_id]

# База данных сделок.
fake_trades = [
    {"id": 1, "user_id": 1, "currency": "BTC", "side": "buy", "price": 123, "amount": 2.12},
    {"id": 2, "user_id": 1, "currency": "BTC", "side": "sell", "price": 125, "amount": 2.12},
]


class Trade(BaseModel):
    """Модель Трейда данных для валидации. Наследуемся от базовой BaseModel.
    id - id трейда, user_id - id usera, currency - валюта, 
    side - сторона, price - стоимость, amount - количество.
    """
    id: int
    user_id: int
    currency: str = Field(max_length=5)
    side: str
    price: float = Field(ge=0)
    amount: float


@app.post("/trades")
def add_trades(trades: List[Trade]):
    """Расширяем список сделок, нашими новыми trade."""
    fake_trades.extend(trades)
    return {"status": 200, "data": fake_trades}
