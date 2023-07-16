import asyncio
from fastapi.responses import JSONResponse
import motor.motor_asyncio
from api.models.todo import Todo
from uuid import UUID, uuid4
from bson import ObjectId, Binary
from pymongo import collection
import json

# Connect to MongoDB
# URL need to be stored on env variable
client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
db = client.TodoList
collection = db.todo

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

# Create a new todo
async def create_todo(todo: Todo):
    todo_data = todo.dict()
    todo_data["id"] = str(todo_data["id"])  # Convert ObjectId to string
    existing_todo = await collection.find_one({"title": todo_data["title"]})
    if existing_todo:
        raise HTTPException(400, "Todo with the same title already exists")

    inserted_result = await collection.insert_one(todo_data)
    if inserted_result.acknowledged:
        return JSONResponse(content=json.dumps(todo_data, cls=CustomJSONEncoder))

# Get all todos
async def get_all_todos():
    todos = await collection.find().to_list(length=None)
    for todo in todos:
        todo["_id"] = str(todo["_id"])  # Convert ObjectId to string
        todo["id"] = todo.pop("_id")  # Rename "_id" to "id"
    return todos

# Get a specific todo by ID
async def get_todo_by_title(title: str):
    todo = await collection.find_one({"title": title})
    if todo:
        todo["_id"] = str(todo["_id"])  # Convert ObjectId to string
    return todo

# Update a todo by ID
async def update_todo_by_title(title: str, new_title: str, new_description: str):
    await collection.update_one(
        {"title": title},
        {"$set": {"title": new_title, "description": new_description}}
    )
    todo = await collection.find_one({"title": title})
    if todo:
        todo["_id"] = str(todo["_id"])  # Convert ObjectId to string
    return todo

# Delete a todo by ID
async def delete_todo(title: str):
    delete_result = await collection.delete_one({"title": title})
    if delete_result.deleted_count:
        return {"message": "Todo deleted successfully"}