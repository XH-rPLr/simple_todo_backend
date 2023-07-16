from pymongo import MongoClient
from bson.objectid import ObjectId
from api.models.todo import Todo

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["todo_app"]
collection = db["todos"]

# Create a new todo
async def create_todo(Todo):
    todo_data = Todo
    await collection.insert_one(todo_data)
    return todo_data

# Get all todos
async def get_all_todos():
    todos = await list(collection.find())
    return todos

# Get a specific todo by ID
async def get_todo_by_id(todo_id):
    todo = await collection.find_one({"_id": ObjectId(todo_id)})
    return todo

# Update a todo by ID
async def update_todo(todo_id, new_title, new_description):
    await collection.update_one(
        {"_id": ObjectId(todo_id)},
        {"$set": {"title": new_title, "description": new_description}}
    )
    todo = await collection.find_one({"_id":ObjectId(todo_id)})
    return todo

# Delete a todo by ID
async def delete_todo(todo_id):
    await collection.delete_one({"_id": ObjectId(todo_id)})
    return True