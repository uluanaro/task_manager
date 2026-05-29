from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_completed: bool = False
    priority: Literal["low", "medium", "high"] = "medium"


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    priority: Literal["low", "medium", "high"] = None

class TaskResponse(TaskBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True