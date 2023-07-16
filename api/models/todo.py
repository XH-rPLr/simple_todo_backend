from pydantic import BaseModel

# Todo model
class Todo(BaseModel):
    id: str
    title: str
    description: str