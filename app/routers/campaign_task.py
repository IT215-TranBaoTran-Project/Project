from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.users import User
from app.schemas.campaign_task import (
    CampaignTaskCreate,
    CampaignTaskUpdate,
    CampaignTaskResponse
)
from app.services.campaign_task import (
    create_campaign_task,
    get_campaign_tasks,
    get_campaign_task,
    update_campaign_task,
    delete_campaign_task
)


router = APIRouter(
    prefix="/campaigns",
    tags=["Campaign Tasks"]
)


@router.post(
    "/{campaign_id}/tasks",
    response_model=CampaignTaskResponse
)
def create_task(
    campaign_id: int,
    task: CampaignTaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_campaign_task(
        db,
        current_user,
        campaign_id,
        task.title,
        task.description,
        task.due_date,
        task.priority,
        task.assignee_id
    )


@router.get(
    "/{campaign_id}/tasks",
    response_model=list[CampaignTaskResponse]
)
def get_tasks(
    campaign_id: int,
    status: str | None = None,
    priority: str | None = None,
    assignee_id: int | None = None,
    search: str | None = None,
    limit: int = 10,
    offset: int = 0,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_campaign_tasks(
        db,
        current_user,
        campaign_id,
        status,
        priority,
        assignee_id,
        search,
        limit,
        offset,
        sort_by,
        sort_order
    )


@router.get(
    "/tasks/{task_id}",
    response_model=CampaignTaskResponse
)
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_campaign_task(
        db,
        current_user,
        task_id
    )


@router.put(
    "/tasks/{task_id}",
    response_model=CampaignTaskResponse
)
def update_task(
    task_id: int,
    task: CampaignTaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return update_campaign_task(
        db,
        current_user,
        task_id,
        task.title,
        task.description,
        task.due_date,
        task.status,
        task.priority,
        task.assignee_id
    )


@router.delete(
    "/tasks/{task_id}"
)
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return delete_campaign_task(
        db,
        current_user,
        task_id
    )