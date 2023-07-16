from pydantic import BaseModel

# Todo model
class Todo(BaseModel):
    title: str
    description: str