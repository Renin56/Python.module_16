from fastapi import FastAPI, Path
from typing import Annotated
import uvicorn


app = FastAPI()

users = {'1': 'Имя: Example, возраст: 18'}

@app.get('/users')
async def get_users() -> dict:
    return users


@app.post('/user/{username}/{age}')
async def add_user(username: str, age: int) -> str:
    user_id = str(int(max(users, key=int)) + 1)
    users[user_id] = f'Имя: {username}, возраст: {age}'
    return f'User {user_id} is registered!'


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: int, username: str, age: int) -> str:
    users[user_id] = f'Имя: {username}, возраст: {age}'
    return f'The user {user_id} is updated.'


@app.delete('/user/{user_id}')
async def delete_user(user_id: str) -> str:
    del users[user_id]
    return f'User {user_id} has been deleted'



if __name__ == '__main__':
    uvicorn.run(app)