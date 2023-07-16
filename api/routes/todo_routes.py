from fastapi import APIRouter
from api.models.todo import Todo
from fastapi import HTTPException
from uuid import UUID

from core.database import (
    create_todo,
    get_all_todos,
    get_todo_by_id,
    update_todo,
    delete_todo
)
router = APIRouter()

# Route to get all todos
@router.get("/todos")
async def get_all_tds():
    response = await get_all_todos()
    return response

# Route to get a single todo by an id
@router.get("/todos/{todo_id}")
async def get_td_by_id(todo_id:UUID):
    response = await get_todo_by_id(todo_id)
    if response:
        return response
    raise HTTPException(404, f"Page not found")

# Route to create a new todo
@router.post("/todos")
async def create_td(todo: Todo):
    response = await create_todo(todo)
    if response:
        return response
    raise HTTPException(400, f"Something went wrong")

# Route to update an existing todo
@router.put("/todos/{todo_id}")
async def update_td(todo_id: str, todo: Todo):
    response = await update_todo(todo_id, todo)
    if response:
        return response
    raise HTTPException(404, f"Page not found")

# Route to delete an existing todo
@router.delete("/todos/{todo_id}")
async def delete_td(todo_id: str):
    response = await delete_todo(todo_id)
    if response:
        return {"message": "Todo deleted successfully"}
    raise HTTPException(404, f"Page not found")
