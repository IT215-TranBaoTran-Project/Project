from fastapi import APIRouter,Depends,HTTPException
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


@router.post("/campaigns/{campaign_id}/campaign-tasks",response_model=CampaignTaskResponse,status_code=201)
def create_campaign_task(
    campaign_id: int,
    task: CampaignTaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()

    if campaign is None:
        raise HTTPException(status_code=404,detail="Không tìm thấy chiến dịch")

    member = db.query(CampaignMember).filter(
        CampaignMember.campaign_id == campaign_id,
        CampaignMember.user_id == current_user.id
    ).first()

    if member is None:
        raise HTTPException(status_code=403,detail="Bạn không phải thành viên của chiến dịch")

    if task.assignee_id:
        assignee = db.query(CampaignMember).filter(
            CampaignMember.campaign_id == campaign_id,
            CampaignMember.user_id == task.assignee_id,
            CampaignMember.position.in_(["CONTENT","ADS","DESIGN"])
        ).first()

        if assignee is None:
            raise HTTPException(status_code=403,detail="Nhân sự được gán không thuộc chiến dịch hoặc không có vị trí hợp lệ")

    new_task = CampaignTask(
        campaign_id=campaign_id,
        assignee_id=task.assignee_id,
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        priority=task.priority
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@router.get("/campaigns/{campaign_id}/campaign-tasks",response_model=list[CampaignTaskResponse])
def get_campaign_tasks(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    member = db.query(CampaignMember).filter(
        CampaignMember.campaign_id == campaign_id,
        CampaignMember.user_id == current_user.id
    ).first()

    if member is None:
        raise HTTPException(status_code=403,detail="Bạn không phải thành viên của chiến dịch")

    return db.query(CampaignTask).filter(
        CampaignTask.campaign_id == campaign_id
    ).all()


@router.get("/campaign-tasks/{task_id}",response_model=CampaignTaskResponse)
def get_campaign_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(CampaignTask).filter(CampaignTask.id == task_id).first()

    if task is None:
        raise HTTPException(status_code=404,detail="Không tìm thấy công việc")

    member = db.query(CampaignMember).filter(
        CampaignMember.campaign_id == task.campaign_id,
        CampaignMember.user_id == current_user.id
    ).first()

    if member is None:
        raise HTTPException(status_code=403,detail="Bạn không phải thành viên của chiến dịch")

    return task


@router.patch("/campaign-tasks/{task_id}",response_model=CampaignTaskResponse)
def update_campaign_task(
    task_id: int,
    task_data: CampaignTaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(CampaignTask).filter(CampaignTask.id == task_id).first()

    if task is None:
        raise HTTPException(status_code=404,detail="Không tìm thấy công việc")

    member = db.query(CampaignMember).filter(
        CampaignMember.campaign_id == task.campaign_id,
        CampaignMember.user_id == current_user.id
    ).first()

    if member is None:
        raise HTTPException(status_code=403,detail="Bạn không phải thành viên của chiến dịch")

    update_data = task_data.model_dump(exclude_unset=True)

    if "assignee_id" in update_data and update_data["assignee_id"]:
        assignee = db.query(CampaignMember).filter(
            CampaignMember.campaign_id == task.campaign_id,
            CampaignMember.user_id == update_data["assignee_id"],
            CampaignMember.position.in_(["CONTENT","ADS","DESIGN"])
        ).first()

        if assignee is None:
            raise HTTPException(status_code=403,detail="Nhân sự được gán không thuộc chiến dịch hoặc không có vị trí hợp lệ")

    for field,value in update_data.items():
        setattr(task,field,value)

    db.commit()
    db.refresh(task)

    return task


@router.delete("/campaign-tasks/{task_id}",status_code=204)
def delete_campaign_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(CampaignTask).filter(CampaignTask.id == task_id).first()

    if task is None:
        raise HTTPException(status_code=404,detail="Không tìm thấy công việc")

    member = db.query(CampaignMember).filter(
        CampaignMember.campaign_id == task.campaign_id,
        CampaignMember.user_id == current_user.id
    ).first()

    if member is None:
        raise HTTPException(status_code=403,detail="Bạn không có quyền xóa công việc này")

    db.delete(task)
    db.commit()

    return None