from celery import Celery

from settings import settings


celery_app = Celery(
    "tasks",
    broker=settings.celery.broker_url,
    backend=settings.celery.result_backend
)


@celery_app.task
def send_webhook_notification(task_id: int, new_status: int):

    # 实际实现应包含：

    # 1. 查询任务关联的webhook URL

    # 2. 发送HTTP POST请求

    # 3. 重试机制和错误处理

    print(f"Sending webhook for task {task_id} with status {new_status}")
    # 示例：requests.post(webhook_url, json={"task_id": task_id, "status": new_status})
