from pymongo import MongoClient
from bson.objectid import ObjectId

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["todo_app"]
collection = db["todos"]

# Create a new todo
def create_todo(title, description):
    todo_data = {"title": title, "description": description}
    result = collection.insert_one(todo_data)
    return result.inserted_id

# Get all todos
def get_all_todos():
    todos = list(collection.find())
    return todos

# Get a specific todo by ID
def get_todo_by_id(todo_id):
    todo = collection.find_one({"_id": ObjectId(todo_id)})
    return todo

# Update a todo by ID
def update_todo(todo_id, new_title, new_description):
    result = collection.update_one(
        {"_id": ObjectId(todo_id)},
        {"$set": {"title": new_title, "description": new_description}}
    )
    return result.modified_count

# Delete a todo by ID
def delete_todo(todo_id):
    result = collection.delete_one({"_id": ObjectId(todo_id)})
    return result.deleted_count
