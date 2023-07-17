from http.client import HTTPException
from uuid import UUID
from fastapi.responses import JSONResponse
from api.models.todo import Todo
from bson import ObjectId, Binary
from pymongo import collection
import json
from api.utils import util
from core import config

db = config.client.TodoList
collection = db.todo

# Create a new todo
async def create_todo(todo: Todo):
    todo_data = todo.dict()
    todo_data["id"] = str(todo_data["id"])  # Convert ObjectId to string
    existing_todo = await collection.find_one({"title": todo_data["title"]})
    if existing_todo:
        raise HTTPException(400, "Todo with the same title already exists")

    inserted_result = await collection.insert_one(todo_data)
    if inserted_result.acknowledged:
        return JSONResponse(content=json.dumps(todo_data, cls=util.CustomJSONEncoder))

# Get all todos
async def get_all_todos():
    todos = await collection.find().to_list(length=None)
    for todo in todos:
        todo["_id"] = str(todo["_id"])  # Convert ObjectId to string
        todo["id"] = todo.pop("_id")  # Rename "_id" to "id"
    return todos

# Get a specific todo by UUID
async def get_todo_by_id(todo_id: UUID):
    todo = await collection.find_one({"id": str(todo_id)})
    if todo:
        todo["_id"] = str(todo["_id"])  # Convert ObjectId to string
    return todo

# Update a todo by UUID
async def update_todo_by_id(todo_id: UUID, new_title: str, new_description: str):
    await collection.update_one(
        {"id": str(todo_id)},
        {"$set": {"title": new_title, "description": new_description}}
    )
    todo = await collection.find_one({"id": str(todo_id)})
    if todo:
        todo["_id"] = str(todo["_id"])  # Convert ObjectId to string
    return todo

# Delete a todo by UUID
async def delete_todo_by_id(todo_id: UUID):
    delete_result = await collection.delete_one({"id": str(todo_id)})
    if delete_result.deleted_count:
        return {"message": "Todo deleted successfully"}