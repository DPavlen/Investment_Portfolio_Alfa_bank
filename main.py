from fastapi import FastAPI

# Далее создаем приложение, которое явл-ся экземпляром FastAPI
app = FastAPI()


# Далее создаем точку входа, для получения данных
@app.get("/")
def hello():
    return "Hello world!"
