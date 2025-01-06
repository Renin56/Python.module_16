from fastapi import FastAPI, Path, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()
template = Jinja2Templates(directory='templates')

users = []


class User(BaseModel):
    id: int = None
    username: str
    age: int


@app.get('/')
async def get_users(request: Request) -> HTMLResponse:
    return template.TemplateResponse('users.html', {'request': request, 'users': users})


@app.get('/user/{user_id}')
async def get_usr(request: Request, user_id: int) -> HTMLResponse:
    return template.TemplateResponse('users.html', {'request': request, 'user': users[user_id]})


# @app.post('/users/{username}/{age}')
@app.post('/users/{username}/{age}')
async def get_user(username: str = Path(min_length=2, max_length=20, description='Enter your name')
                   , age: int = Path(ge=10, le=120)) -> str:

    current_index = len(users)
    user = User(id=current_index, username=username, age=age)
    users.append(user)

    return str(user)


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: int = Path(ge=0, le=100), username: str = Path(min_length=2, max_length=20
    , description='Enter your name'), age: int = Path(le=120)) -> str:

    try:
        user = users[user_id]
        if user:
            user.username = username
            user.age = age
            return str(user)
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/users/{user_id}')
async def delete_user(user_id: int = Path(ge=1, le=100, description='Delete user')) -> str:
    try:
        user = users[user_id]
        if user:
            users.pop(user_id)
            return str(user)
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')


if __name__ == "__main__":
    uvicorn.run(app)
