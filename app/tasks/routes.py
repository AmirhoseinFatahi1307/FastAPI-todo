from fastapi import APIRouter, Path, Depends, HTTPException, Body, Query, status
from fastapi.responses import JSONResponse
from tasks.schemas import *
from tasks.models import Task_models
from sqlalchemy.orm import Session
from core.database import get_db
from typing import List

router = APIRouter(tags=["Tasks"], prefix="/Todo")


@router.get("/Tasks", response_model=List[TaskResponseSchema])
async def retrieve_task_list(
    completed: bool = Query(
        None, description="Filter tasks based on the Completion status"
    ),
    limit: int = Query(
        default=10, gt=0, le=50, description="Maximum number of items returned per page"
    ),
    offset: int = Query(
        default=0, ge=0, description="Number of items to skip before returning results"
    ),
    db: Session = Depends(get_db),
):
    query = db.query(Task_models)
    if completed is not None:
        query = query.filter_by(is_completed=completed)
    return query.limit(limit).offset(offset).all()


@router.get("/Tasks/{task_id}", response_model=TaskResponseSchema)
async def retrieve_task_detail(
    task_id: int = Path(
        deprecated=True,
        description="It will be searched with the title you provided",
        gt=0,
    ),
    db: Session = Depends(get_db),
):
    query = db.query(Task_models).filter_by(id=task_id).first()
    if not query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return query


@router.post(
    "/Tasks", status_code=status.HTTP_201_CREATED, response_model=TaskResponseSchema
)
async def create_task(
    request: TaskCreateSchema,
    db: Session = Depends(get_db),
):
    task_obj = Task_models(**request.model_dump())
    db.add(task_obj)
    db.commit()
    db.refresh(task_obj)
    return task_obj


@router.put(
    "/Tasks/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskUpdateSchema
)
async def updating_task_detail(
    request: TaskUpdateSchema = Body(),
    task_id: int = Path(
        deprecated=True,
        description="It will be searched with the title you provided",
        gt=0,
    ),
    db: Session = Depends(get_db),
):
    task = db.query(Task_models).filter_by(id=task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    update_date = request.model_dump(exclude_unset=True)
    for field, value in update_date.items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


@router.delete("/Tasks/{task_id}")
async def deleting_task(task_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    task = db.query(Task_models).filter_by(id=task_id).one_or_none()
    if task:
        db.delete(task)
        db.commit()
        return JSONResponse(content={"Detai": "Task removed succssesfully"})
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
