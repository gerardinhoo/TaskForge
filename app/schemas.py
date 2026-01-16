from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


# ---------- Tags ----------
class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    """Payload when creating a new tag."""
    pass


class Tag(TagBase):
    id: int

    class Config:
        orm_mode = True


# ---------- Tasks ----------
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    """Payload when creating a new task."""
    tag_ids: List[int] = []

class TaskUpdate(BaseModel):
    """Payload when updating an existing task."""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[datetime] = None
    tag_ids: Optional[List[int]] = None

class Task(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime
    tags: List[Tag] = []

    class Config:
        orm_mode = True
