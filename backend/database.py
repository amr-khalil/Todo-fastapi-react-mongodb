import os
import motor.motor_asyncio # MongoDB driver
from fastapi import HTTPException

from models import Todo

# Create a MongoDB client
mongodb_url = os.getenv("mongodb_url")
client = motor.motor_asyncio.AsyncIOMotorClient(mongodb_url)

# Create database
database = client.TodoList

# Create a collection
collection = database.todo

async def read_one_todo(title):
    document = await collection.find_one({"title":title}, {"_id":0})
    return document

async def read_all_todos():
    todos = []
    cursor = collection.find({})
    async for document in cursor:
        todos.append(Todo(**document))
    return todos

async def create_todo(todo):
    if await collection.find_one({"title":todo['title']}):
        raise HTTPException(200, "This values is alread exist!")
    await collection.insert_one(todo)
    return f"Todo Item '{todo['title']}' was created successfully."


async def update_todo(title, desc):
    await collection.update_one(
        {"title":title},
        {"$set":{"description":desc}}
        )
    document = await collection.find_one({"title":title})
    return document

async def remove_todo(title):
    await collection.delete_one(
        {"title":title}    
    )
    
    return True