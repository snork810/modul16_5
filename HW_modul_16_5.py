from fastapi import FastAPI, Path, status, HTTPException, Request,Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Annotated, List

app = FastAPI()
templates = Jinja2Templates(directory='HW_templates')
users = []
class User(BaseModel):
    id: int = None
    username: str
    age: int

@app.get('/')

async def main_page(request:Request)->HTMLResponse:
    return templates.TemplateResponse('HW_users.html', {'request':request, 'users':users})

@app.get('/user/{user_id}')
async def get_user_info(request:Request, user_id:int) -> HTMLResponse:
    try:
        return templates.TemplateResponse('HW_users.html', {'request':request, 'user':users[user_id]})
    except IndexError:
        raise HTTPException(status_code=404, detail='User not found')

@app.post('/user/{username}/{age}')
async def create_user(user:User, username:Annotated[str, Path(min_length=6, max_length=15, description="Enter your name:", example="Viktor")],
                      age:Annotated[int, Path(ge=18, le=120, description="Enter your age:", example='24')])->str:
    user.id = len(users)
    user.username = username
    user.age = age
    users.append(user)
    return f"User №{user.id} is registered"

@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id:Annotated[int, Path(ge=1, le=500, description="Enter userID what you want to edit")], 
                      username:Annotated[str, Path(min_length=6, max_length=15, description="Enter new name:", example="Viktor")],
                      age:Annotated[int, Path(ge=18, le=120, description="Enter new age:", example='24')])->str:
    try:
        edit_user = users[user_id-1]
        edit_user.username = username
        edit_user.age = age
        return f"The User {user_id} is updated"
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')

@app.delete('/user/{user_id}')
async def user_delete(user_id:Annotated[int, Path(ge=1, le=500, description="Enter userID what you want to edit")])->str:
    try:
        users.pop(user_id-1)
        return f"The User {user_id} is deleted"
    except IndexError:
        raise HTTPException(status_code=404, detail='User not found')