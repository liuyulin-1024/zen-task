from fastapi import APIRouter, Depends, HTTPException
from tortoise.contrib.pydantic import pydantic_model_creator

from core.models import Task, User
from tools.common import get_logger
from core.middlewares import authentication
from .celery_worker import send_webhook_notification

router = APIRouter()
logger = get_logger()

Task_Pydantic = pydantic_model_creator(Task, name="Task")
TaskIn_Pydantic = pydantic_model_creator(Task, name="TaskIn", exclude_readonly=True)


# 创建新任务
@router.post("/tasks")
async def create_task(
        task: TaskIn_Pydantic,
        user: User = Depends(authentication)
):
    task_data = task.dict()
    task_data["owner"] = user.id
    task_obj = await Task.create(**task_data)
    return await Task_Pydantic.from_tortoise_orm(task_obj)


# 获取任务列表（分页+过滤）

@router.get("/tasks")
async def list_tasks(
        status: int = None,
        owner: int = None,
        page: int = 1,
        per_page: int = 10,
        user: User = Depends(authentication)
):
    query = Task.all()
    if status:
        query = query.filter(status=status)
    if owner:
        query = query.filter(owner=owner)
    tasks = await query.offset((page - 1) * per_page).limit(per_page)
    total = await query.count()
    return {
        "items": [await Task_Pydantic.from_tortoise_orm(t) for t in tasks],
        "total": total,
        "page": page
    }


# 更新任务状态（触发Webhook）
@router.put("/tasks/{task_id}")
async def update_task(
        task_id: int,
        task_update: TaskIn_Pydantic,
        user: User = Depends(authentication)
):
    task = await Task.get_or_none(id=task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    # 权限检查
    if task.owner != user["id"] and not user["is_admin"]:
        raise HTTPException(403, "No permission")

    # 状态变更时触发通知
    if task_update.status != task.status:
        send_webhook_notification.delay(task_id, task_update.status)

    await task.update_from_dict(task_update.dict())
    await task.save()
    return await Task_Pydantic.from_tortoise_orm(task)
