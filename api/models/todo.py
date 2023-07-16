from pydantic import BaseModel, Field, UUID4
from uuid import UUID, uuid4
# Todo model
class Todo(BaseModel):
    id: UUID = Field(default_factory=uuid4, read_only=True)
    title: str
    description: str
