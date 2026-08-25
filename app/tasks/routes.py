from fastapi import APIRouter

router = APIRouter(tags=["Tasks"], prefix="/Todo")


@router.get("/Tasks")
async def retrieve_task_list():
    return []


@router.get("/Task/{Task_id}")
async def retrieve_task_detail(Task_id: int):
    return []
