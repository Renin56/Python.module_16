from fastapi import FastAPI
import uvicorn


app = FastAPI()

@app.get('/')
async def root() -> str:
    return 'Главная страница'

@app.get('/user/admin')
async def page_admin() -> str:
    return 'Вы вошли как администратор'

@app.get('/user/{user_id}')
async def page_user_id(user_id: int) -> str:
    return f'Вы вошли как пользователь № {user_id}'

@app.get('/user')
async def random_user(username: str, age: int) -> str:
    return f'Информация о пользователе. Имя: {username} , Возраст: {age}'


if __name__ == '__main__':
    uvicorn.run(app)