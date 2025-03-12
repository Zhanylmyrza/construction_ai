from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TaskBase(BaseModel):
    name: str
    status: str

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    pass

class ProjectBase(BaseModel):
    project_name: str
    location: str

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    status: str
    tasks: List[TaskResponse]

    class Config:
        from_attributes = True  # Updated from orm_mode in pydantic v2