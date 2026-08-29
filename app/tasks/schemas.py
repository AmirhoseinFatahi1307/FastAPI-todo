from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskBaseSchema(BaseModel):
    title: str = Field(
        ..., max_length=150, min_length=2, description="title of the task"
    )
    description: Optional[str] = Field(
        None, max_length=500, description="title of the task"
    )
    is_completed: bool = Field(..., description="State of the task")


class TaskCreateSchema(TaskBaseSchema):
    pass


class TaskUpdateSchema(BaseModel):
    title: Optional[str] = Field(
        None, max_length=150, min_length=2, description="title of the task"
    )
    description: Optional[str] = Field(
        None, max_length=500, description="description of the task"
    )
    is_completed: Optional[bool] = Field(None, description="State of the task")


class TaskResponseSchema(TaskBaseSchema):
    id: int = Field(..., description="Unique identifier of the object")

    create_date: datetime = Field(
        ..., description="Creation date and time of the object"
    )
    update_date: datetime = Field(
        ..., description="Updating date and time of the object"
    )
