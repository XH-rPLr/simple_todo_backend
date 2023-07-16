# Import required libraries
from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel

# Create FastAPI instance
app = FastAPI()

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["todo_app"]
collection = db["todos"]

# Todo model
class Todo(BaseModel):
    title: str
    description: str

# Route to get all todos
@app.get("/todos")
def get_all_todos():
    todos = list(collection.find())
    return todos

# Route to create a new todo
@app.post("/todos")
def create_todo(todo: Todo):
    todo_data = {"title": todo.title, "description": todo.description}
    result = collection.insert_one(todo_data)
    return {"message": "Todo created successfully", "id": str(result.inserted_id)}

# Route to update an existing todo
@app.put("/todos/{todo_id}")
def update_todo(todo_id: str, todo: Todo):
    todo_data = {"title": todo.title, "description": todo.description}
    result = collection.update_one({"_id": todo_id}, {"$set": todo_data})
    if result.modified_count == 1:
        return {"message": "Todo updated successfully"}
    else:
        return {"message": "Todo not found"}

# Route to delete an existing todo
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: str):
    result = collection.delete_one({"_id": todo_id})
    if result.deleted_count == 1:
        return {"message": "Todo deleted successfully"}
    else:
        return {"message": "Todo not found"}

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
