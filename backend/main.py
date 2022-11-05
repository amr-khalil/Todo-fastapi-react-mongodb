from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from database import (Todo, read_all_todos, read_one_todo, create_todo, update_todo, remove_todo)
from models import Todo

# App object
app = FastAPI()


origins = ['http://localhost:3000']
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials= True,
    allow_methods = ['*'],
    allow_headers = ['*']
)

@app.get('/')
def read_root():
    return {"status":"OK"}


@app.get("/api/todo")
async def get_todo():
    response = await read_all_todos()
    return response

@app.get("/api/todo/{title}")
async def get_todo_by_id(title:str):
    response = await read_one_todo(title)
    if response:
        return response
    raise HTTPException(404, f"There is no Todo item with this title {title}")

@app.post("/api/todo")
async def post_todo(todo:Todo):
    response = await create_todo(todo.dict())
    if response:
        return response
    raise HTTPException(400, "Someting went bad / Bas request")

@app.put("/api/todo/{title}", response_model=Todo)
async def put_todo(title:str, desc:str):
    response = await update_todo(title, desc)
    if response:
        return response
    raise HTTPException(404, f"There is no Todo item with this title {title}")

@app.delete("/api/todo/{title}")
async def delete_todo(title:str):
    response = await remove_todo(title)
    if response:
        return f"Successfully deleted tod item {title}"
    raise HTTPException(404, f"There is no Todo item with this title {title}")
    
    
    