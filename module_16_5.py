from fastapi import FastAPI, Path, HTTPException, Body, Request
from fastapi.responses import HTMLResponse
from typing import Annotated
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory='templates')

app = FastAPI()

users = []

class User(BaseModel):
    id: int = None
    username: str
    age: int


@app.get("/")
async def get_all_message(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get('/users/{user_id}')
async def get_users(request: Request, user_id: int) -> HTMLResponse:
    try:
        return templates.TemplateResponse("users.html", {"request": request, "user": users[user_id-1]})
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')


@app.post('/user/{username}/{age}')
async def post_users(user: User,
                     username: Annotated[str, Path(min_length=3, max_length=20, description="Enter username",
                                                   example='UrbanUser')],
                     age: Annotated[int, Path(ge=18, le=120, description="Enter age", example="24")]) -> str:
    if users is None:
        user.id = 1
    else:
        user.id = len(users) + 1
    user.username = username
    user.age = age
    users.append(user)
    return f"User {username} is registered"


@app.put('/user/{user_id}/{username}/{age}')
async def update_users(user_id: Annotated[int, Path(description="Enter User ID", example='1')],
                       username: Annotated[str, Path(min_length=3, max_length=20, description="Enter username",
                                                     example='UrbanUser')],
                       age: Annotated[int, Path(ge=18, le=120, description="Enter age", example="24")],
                       user: str = Body()) -> str:
    try:
        edit_user_id = users[user_id-1]
        edit_user_id.username = user
        edit_user_id.age = age
        return f"User {username} has been updated"
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')


@app.delete("/user/{user_id}")
async def delete_users(user_id: int = Path(description="Enter User ID", example='1')) -> str:
    try:
        users.pop(user_id-1)
        return f"User {user_id} has been deleted"
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')
