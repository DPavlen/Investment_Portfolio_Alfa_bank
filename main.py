from fastapi import FastAPI

# Далее создаем приложение, которое явл-ся экземпляром FastAPI,  зададим ему понятное имя
app = FastAPI(
    title="Traiding App"
)

# База данных пользователей. Соответсвенно у каждого есть id
fake_users = [
    {"id": 1, "role": "admin", "name": "Bob"},
    {"id": 2, "role": "investor", "name": "John"},
    {"id": 3, "role": "trader", "name": "Matt"},
]

# Далее создаем точку входа, для получения данных о пользователе # Оборачиваем в фигурные скобки {user_id} и далее в функции 
# get_user получаем параметр user_id и необходимо получить # конкретного пользователя с list_comprehesions
@app.get("/users/{user_id}")
def get_user(user_id: int):
    """Получаем по id текущего usera."""
    return [user for user in fake_users if user.get("id") == user_id]

# База данных сделок.
fake_trades = [
    {"id": 1, "user_id": 1, "currency": "BTC", "side": "buy", "price": 123, "amount": 2.12},
    {"id": 2, "user_id": 1, "currency": "BTC", "side": "sell", "price": 125, "amount": 2.12},
]


@app.get("/trades")
def get_trades(limit: int = 1, offset: int = 0):
    """Параметры: limit-количество получаемых сделок
    offset-сдвиг(например если хотим получить 2-ю, то надо 1)."""
    return fake_trades[offset:][:limit]


# База данных пользователей fake_users2.
fake_users2 = [
    {"id": 1, "role": "admin", "name": "Bob"},
    {"id": 2, "role": "investor", "name": "John"},
    {"id": 3, "role": "trader", "name": "Matt"},
]

@app.post("/users/{user_id}")
def change_user_name(user_id: int, new_name: str):
    """Итератор filter, с анонимной функцией lambda и итерируемый объект 
    список словарей fake_users2 и берем 0(т.е. id=1). Далее итератор оборачиваем в list."""
    current_user = list(filter(lambda user: user.get("id") == user_id, fake_users2))[0]
    # Далее пользователю сменим name.
    current_user["name"] = new_name
    # Далее по стандарту возвращаем HTTP код и данные
    return {"staus": 200, "data": current_user}