import motor.motor_asyncio
from api.models.todo import Todo
from uuid import UUID
from bson import ObjectId

# Connect to MongoDB
# URL need to be stored on env variable
client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
db = client.TodoList
collection = db.todo

# Create a new todo
async def create_todo(todo: Todo):
    todo_data = todo.dict()
    inserted_result = await collection.insert_one(todo_data)
    if inserted_result.acknowledged:
        todo_data["_id"] = str(inserted_result.inserted_id)  # Convert ObjectId to string
        return todo_data

# Get all todos
async def get_all_todos():
    todos = await collection.find().to_list(length=None)
    for todo in todos:
        todo["_id"] = str(todo["_id"])  # Convert ObjectId to string
        todo["id"] = todo.pop("_id")  # Rename "_id" to "id"
    return todos

# Get a specific todo by ID
async def get_todo_by_id(todo_id:UUID):
    todo = await collection.find_one({"_id": todo_id})
    if todo:
        todo["_id"] = str(todo["_id"])  # Convert ObjectId to string
    return todo

# Update a todo by ID
async def update_todo(todo_id: UUID, new_title, new_description):
    await collection.update_one(
        {"_id": str(todo_id)},
        {"$set": {"title": new_title, "description": new_description}}
    )
    todo = await collection.find_one({"id":str(todo_id)})
    if todo:
        todo["_id"] = str(todo["_id"])  # Convert ObjectId to string
    return todo

# Delete a todo by ID
async def delete_todo(todo_id: UUID):
    delete_result = await collection.delete_one({"id": str(todo_id)})
    if delete_result.deleted_count:
        return {"message": "Todo deleted successfully"}