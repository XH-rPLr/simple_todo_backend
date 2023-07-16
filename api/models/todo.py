from pydantic import BaseModel, Field, UUID4
from uuid import UUID, uuid4
# Todo model
class Todo(BaseModel):
    id: UUID4 = Field(default_factory=uuid4, alias="_id")
    title: str
    description: str