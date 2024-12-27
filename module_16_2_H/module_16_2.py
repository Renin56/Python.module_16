from fastapi import FastAPI, Path
from typing import Annotated
import uvicorn


app = FastAPI()

@app.get('/')
async def root() -> str:
    return 'Главная страница'

@app.get('/user/admin')
async def page_admin() -> str:
    return 'Вы вошли как администратор'

@app.get('/user/{user_id}')
async def page_user_id(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='10')]) -> str:
    return f'Вы вошли как пользователь № {user_id}'

@app.get('/user/{username}/{age}')
async def random_user(username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
                      age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='24')]) -> str:
    return f'Информация о пользователе. Имя: {username} , Возраст: {age}'


if __name__ == '__main__':
    uvicorn.run(app)