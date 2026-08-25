from fastapi import APIRouter

router = APIRouter()


@router.get("/tasks")
async def retrive_task_list():
    return []
