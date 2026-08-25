from typing import Literal

from fastapi import APIRouter,Depends,HTTPException,Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.users import User
from app.models.campaigns import Campaign,CampaignMember,CampaignTask
from app.schemas.campaigns import CampaignTaskCreate,CampaignTaskUpdate,CampaignTaskResponse


router = APIRouter(
    prefix="",
    tags=["Campaign Tasks"]
)


@router.post(
    "/campaigns/{campaign_id}/campaign-tasks",
    response_model=CampaignTaskResponse,
    status_code=201
)
def create_campaign_task(
    campaign_id: int,
    task: CampaignTaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id
    ).first()

    if campaign is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy chiến dịch"
        )

    member = db.query(CampaignMember).filter(
        CampaignMember.campaign_id == campaign_id,
        CampaignMember.user_id == current_user.id
    ).first()

    if campaign.owner_id != current_user.id and member is None:
        raise HTTPException(
            status_code=403,
            detail="Bạn không có quyền tạo công việc"
        )

    if task.assignee_id is not None:
        assignee = db.query(CampaignMember).filter(
            CampaignMember.campaign_id == campaign_id,
            CampaignMember.user_id == task.assignee_id
        ).first()

        if assignee is None:
            raise HTTPException(
                status_code=403,
                detail="Người được giao không thuộc chiến dịch"
            )

        if assignee.position not in ["CONTENT","ADS","DESIGN"]:
            raise HTTPException(
                status_code=403,
                detail="Người được giao phải thuộc bộ phận CONTENT, ADS hoặc DESIGN"
            )

    new_task = CampaignTask(
        campaign_id=campaign_id,
        assignee_id=task.assignee_id,
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        status="TODO",
        priority=task.priority
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@router.get(
    "/campaigns/{campaign_id}/campaign-tasks",
    response_model=list[CampaignTaskResponse]
)
def get_campaign_tasks(
    campaign_id: int,
    status: str | None = Query(default=None),
    priority: str | None = Query(default=None),
    assignee_id: int | None = Query(default=None),
    search: str | None = Query(default=None),
    limit: int = Query(default=10,ge=1,le=100),
    offset: int = Query(default=0,ge=0),
    sort_by: Literal["created_at","due_date"] = "created_at",
    sort_order: Literal["asc","desc"] = "desc",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id
    ).first()

    if campaign is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy chiến dịch"
        )

    member = db.query(CampaignMember).filter(
        CampaignMember.campaign_id == campaign_id,
        CampaignMember.user_id == current_user.id
    ).first()

    if campaign.owner_id != current_user.id and member is None:
        raise HTTPException(
            status_code=403,
            detail="Bạn không phải thành viên của chiến dịch"
        )

    if status is not None and status not in ["TODO","IN_PROGRESS","DONE"]:
        raise HTTPException(
            status_code=400,
            detail="Status phải là TODO, IN_PROGRESS hoặc DONE"
        )

    if priority is not None and priority not in ["LOW","MEDIUM","HIGH"]:
        raise HTTPException(
            status_code=400,
            detail="Priority phải là LOW, MEDIUM hoặc HIGH"
        )

    query = db.query(CampaignTask).filter(
        CampaignTask.campaign_id == campaign_id
    )

    if status is not None:
        query = query.filter(
            CampaignTask.status == status
        )

    if priority is not None:
        query = query.filter(
            CampaignTask.priority == priority
        )

    if assignee_id is not None:
        query = query.filter(
            CampaignTask.assignee_id == assignee_id
        )

    if search is not None:
        query = query.filter(
            CampaignTask.title.ilike(f"%{search}%")
        )

    if sort_by == "created_at":
        sort_column = CampaignTask.created_at
    else:
        sort_column = CampaignTask.due_date

    if sort_order == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    return query.offset(offset).limit(limit).all()


@router.get(
    "/campaign-tasks/{task_id}",
    response_model=CampaignTaskResponse
)
def get_campaign_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(CampaignTask).filter(
        CampaignTask.id == task_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy công việc"
        )

    campaign = db.query(Campaign).filter(
        Campaign.id == task.campaign_id
    ).first()

    if campaign is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy chiến dịch"
        )

    member = db.query(CampaignMember).filter(
        CampaignMember.campaign_id == task.campaign_id,
        CampaignMember.user_id == current_user.id
    ).first()

    if campaign.owner_id != current_user.id and member is None:
        raise HTTPException(
            status_code=403,
            detail="Bạn không thuộc chiến dịch này"
        )

    return task


@router.patch(
    "/campaign-tasks/{task_id}",
    response_model=CampaignTaskResponse
)
def update_campaign_task(
    task_id: int,
    task_data: CampaignTaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(CampaignTask).filter(
        CampaignTask.id == task_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy công việc"
        )

    campaign = db.query(Campaign).filter(
        Campaign.id == task.campaign_id
    ).first()

    if campaign is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy chiến dịch"
        )

    member = db.query(CampaignMember).filter(
        CampaignMember.campaign_id == task.campaign_id,
        CampaignMember.user_id == current_user.id
    ).first()

    is_owner = campaign.owner_id == current_user.id
    is_assignee = task.assignee_id == current_user.id

    if not is_owner and not is_assignee:
        if member is None:
            raise HTTPException(
                status_code=403,
                detail="Bạn không thuộc chiến dịch này"
            )

        raise HTTPException(
            status_code=403,
            detail="Bạn không có quyền cập nhật công việc"
        )

    update_data = task_data.model_dump(exclude_unset=True)

    if "assignee_id" in update_data:
        new_assignee_id = update_data["assignee_id"]

        if new_assignee_id is not None:
            assignee = db.query(CampaignMember).filter(
                CampaignMember.campaign_id == task.campaign_id,
                CampaignMember.user_id == new_assignee_id
            ).first()

            if assignee is None:
                raise HTTPException(
                    status_code=403,
                    detail="Người được giao không thuộc chiến dịch"
                )

            if assignee.position not in ["CONTENT","ADS","DESIGN"]:
                raise HTTPException(
                    status_code=403,
                    detail="Người được giao phải thuộc bộ phận CONTENT, ADS hoặc DESIGN"
                )

    for field,value in update_data.items():
        setattr(task,field,value)

    db.commit()
    db.refresh(task)

    return task


@router.delete(
    "/campaign-tasks/{task_id}",
    status_code=204
)
def delete_campaign_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(CampaignTask).filter(
        CampaignTask.id == task_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy công việc"
        )

    campaign = db.query(Campaign).filter(
        Campaign.id == task.campaign_id
    ).first()

    if campaign is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy chiến dịch"
        )

    if campaign.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Chỉ chủ chiến dịch mới có quyền xóa công việc"
        )

    db.delete(task)
    db.commit()

    return None