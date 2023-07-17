import json
import uuid
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from api.models.todo import Todo
from fastapi import HTTPException

from core.database import (
    create_todo,
    get_all_todos,
    get_todo_by_id,
    update_todo_id,
    delete_todo_by_id
)
router = APIRouter()

@router.get("/todos")
async def get_all_tds():
    response = await get_all_todos()
    encoded_response = json.dumps(response, ensure_ascii=False).encode('utf-8')
    return JSONResponse(content=encoded_response.decode('utf-8'))

@router.get("/todos/{todo_id}")
async def get_todo_by_id_route(todo_id: uuid):
    response = await get_todo_by_id(todo_id)
    if response:
        return response
    raise HTTPException(404, "Todo not found")

# Route to create a new todo
@router.post("/todos")
async def create_td(todo: Todo):
    response = await create_todo(todo)
    if response:
        return response
    raise HTTPException(400, f"Something went wrong")

# Route to update an existing todo
@router.put("/todos/{todo_id}")
async def update_todo_route(todo_id: UUID, todo: Todo):
    response = await update_todo_by_id(todo_id, todo.title, todo.description)
    if response:
        return response
    raise HTTPException(404, "Todo not found")

# Route to delete an existing todo
@router.delete("/todos/{todo_id}")
async def delete_todo_route(todo_id: UUID):
    response = await delete_todo_by_id(todo_id)
    if response:
        return response
    raise HTTPException(404, "Todo not found")