from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn


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
async def add_user(username: str, age: int) -> User:
    user_id = max((u.id for u in users), default=0) + 1
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: int, username: str, age: int) -> User:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}')
async def delete_user(user_id: int) -> User:
    for i, u in enumerate(users):
        if u.id == user_id:
            return users.pop(i)
    raise HTTPException(status_code=404, detail="User was not found")



if __name__ == '__main__':
    uvicorn.run(app)