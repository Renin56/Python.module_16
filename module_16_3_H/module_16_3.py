from fastapi import FastAPI, Path, HTTPException
from typing import Annotated
import uvicorn


app = FastAPI()

users = {'1': 'Имя: Example, возраст: 18'}


@app.get('/users')
async def get_users() -> dict:
    return users


@app.post('/user/{username}/{age}')
async def add_user(username: Annotated[str, Path(min_length=3, max_length=20, description='Введите имя пользователя')],
                   age: Annotated[int, Path(ge=18, le=70, description='Укажите возраст пользователя')]) -> str:
    user_id = str(int(max(users, key=int)) + 1)
    users[user_id] = f'Имя: {username}, возраст: {age}'
    return f'User {user_id} is registered!'


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: Annotated[int, Path(ge=1, le=100, description='Введите ID пользователя от 1 до 100')],
                      username: Annotated[str, Path(min_length=3, max_length=20, description='Введите имя пользователя')],
                      age: Annotated[int, Path(ge=18, le=70, description='Укажите возраст пользователя')]) -> str:
    user = users.get(str(user_id), None)
    print(user)

    if user:
        users[user_id] = f'Имя: {username}, возраст: {age}'
        return f'The user {user_id} is updated.'

    raise HTTPException(status_code=404, detail='Пользователь не найден')


@app.delete('/user/{user_id}')
async def delete_user(user_id: Annotated[int, Path(ge=1, le=100, description='Введите ID пользователя от 1 до 100')]) -> str:
    user = users.get(str(user_id), None)

    if user:
        users.pop(str(user_id), None)
        return f'User {user_id} has been deleted'

    raise HTTPException(status_code=404, detail='Пользователь не найден')


if __name__ == '__main__':
    uvicorn.run(app)
