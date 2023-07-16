from fastapi import APIRouter
from api.models.todo import Todo
from fastapi import HTTPException

router = APIRouter()

# Route to get all todos
@router.get("/todos")
def get_all_todos():
    todos = list(collection.find())
    return todos

# Route to create a new todo
@router.post("/todos")
def create_todo(todo: Todo):
    todo_data = {"title": todo.title, "description": todo.description}
    result = collection.insert_one(todo_data)
    return {"message": "Todo created successfully", "id": str(result.inserted_id)}

# Route to update an existing todo
@router.put("/todos/{todo_id}")
def update_todo(todo_id: str, todo: Todo):
    todo_data = {"title": todo.title, "description": todo.description}
    result = collection.update_one({"_id": todo_id}, {"$set": todo_data})
    if result.modified_count == 1:
        return {"message": "Todo updated successfully"}
    else:
        return {"message": "Todo not found"}

# Route to delete an existing todo
@router.delete("/todos/{todo_id}")
def delete_todo(todo_id: str):
    result = collection.delete_one({"_id": todo_id})
    if result.deleted_count == 1:
        return {"message": "Todo deleted successfully"}
    else:
        return {"message": "Todo not found"}