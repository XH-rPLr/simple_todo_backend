import json
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from api.models.todo import Todo
from fastapi import HTTPException

from core.database import (
    create_todo,
    get_all_todos,
    get_todo_by_title,
    update_todo_by_title,
    delete_todo
)
router = APIRouter()

@router.get("/todos")
async def get_all_tds():
    response = await get_all_todos()
    encoded_response = json.dumps(response, ensure_ascii=False).encode('utf-8')
    return JSONResponse(content=encoded_response.decode('utf-8'))

# Route to get a single todo by an title
@router.get("/todos/{todo_title}")
async def get_td_by_title(title: str):
    response = await get_todo_by_title(title)
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
@router.put("/todos/{title}")
async def update_todo_route(title: str, todo: Todo):
    response = await update_todo_by_title(title, todo.title, todo.description)
    if response:
        return response
    raise HTTPException(404, f"Todo not found")

# Route to delete an existing todo
@router.delete("/todos/{title}")
async def delete_td(title: str):
    """Delete a todo by title."""
    response = await delete_todo(title)
    if response:
        return response
    raise HTTPException(404, f"Page not found")
