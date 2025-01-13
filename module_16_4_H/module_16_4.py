from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from typing import List
import uvicorn
from typing_extensions import Annotated


app = FastAPI()

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get('/users')
async def get_users() -> List[User]:
    return users


@app.post('/user/{username}/{age}')
async def add_user(username: Annotated[str, Path(min_length=3, max_length=20, description='Введите имя')],
                   age: Annotated[int, Path(ge=18, le=100, description='Укажите возраст')]) -> User:

    user_id = max((user.id for user in users), default=0) + 1
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)

    return new_user


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: Annotated[int, Path(ge=1, le=100, description='Введите ID пользователя от 1 до 100')],
                      username: Annotated[str, Path(min_length=3, max_length=20, description='Введите имя пользователя')],
                      age: Annotated[int, Path(ge=18, le=70, description='Укажите возраст пользователя')]) -> User:

    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user

    raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}')
async def delete_user(user_id: Annotated[int, Path(ge=1, le=100, description='Введите ID пользователя от 1 до 100')]) -> User:

    for i, user in enumerate(users):
        if user.id == user_id:
            return users.pop(i)

    raise HTTPException(status_code=404, detail="User was not found")



if __name__ == '__main__':
    uvicorn.run(app)
