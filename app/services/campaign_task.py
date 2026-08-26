from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.campaigns import Campaign, CampaignMember
from app.models.campaign_tasks import CampaignTask
from app.models.users import User


VALID_STATUS = [
    "TODO",
    "IN_PROGRESS",
    "DONE"
]

VALID_PRIORITY = [
    "LOW",
    "MEDIUM",
    "HIGH"
]

VALID_POSITIONS = [
    "CONTENT",
    "ADS",
    "DESIGN"
]


def get_campaign_and_member(
    db: Session,
    campaign_id: int,
    user_id: int
):
    campaign = (
        db.query(Campaign)
        .filter(Campaign.id == campaign_id)
        .first()
    )

    if campaign is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy chiến dịch"
        )

    member = (
        db.query(CampaignMember)
        .filter(
            CampaignMember.campaign_id == campaign_id,
            CampaignMember.user_id == user_id
        )
        .first()
    )

    if (
        campaign.owner_id != user_id
        and member is None
    ):
        raise HTTPException(
            status_code=403,
            detail="Bạn không phải thành viên của chiến dịch"
        )

    return campaign, member


def validate_assignee(
    db: Session,
    campaign_id: int,
    assignee_id: int
):
    user = (
        db.query(User)
        .filter(User.id == assignee_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy người được giao"
        )

    member = (
        db.query(CampaignMember)
        .filter(
            CampaignMember.campaign_id == campaign_id,
            CampaignMember.user_id == assignee_id
        )
        .first()
    )

    if member is None:
        raise HTTPException(
            status_code=403,
            detail="Người được giao không thuộc chiến dịch"
        )

    if member.position not in VALID_POSITIONS:
        raise HTTPException(
            status_code=403,
            detail="Người được giao không có position hợp lệ"
        )


def create_campaign_task(
    db: Session,
    current_user: User,
    campaign_id: int,
    title: str,
    description: str,
    due_date,
    priority: str,
    assignee_id: int
):
    get_campaign_and_member(
        db,
        campaign_id,
        current_user.id
    )

    if not title or not title.strip():
        raise HTTPException(
            status_code=400,
            detail="Tên công việc không được để trống"
        )

    if len(title.strip()) > 255:
        raise HTTPException(
            status_code=400,
            detail="Tên công việc không được vượt quá 255 ký tự"
        )

    if priority not in VALID_PRIORITY:
        raise HTTPException(
            status_code=400,
            detail="Priority không hợp lệ"
        )

    validate_assignee(
        db,
        campaign_id,
        assignee_id
    )

    task = CampaignTask(
        campaign_id=campaign_id,
        title=title.strip(),
        description=description,
        due_date=due_date,
        status="TODO",
        priority=priority,
        assignee_id=assignee_id
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_campaign_tasks(
    db: Session,
    current_user: User,
    campaign_id: int,
    status: str | None = None,
    priority: str | None = None,
    assignee_id: int | None = None,
    search: str | None = None,
    limit: int = 10,
    offset: int = 0,
    sort_by: str = "created_at",
    sort_order: str = "desc"
):
    get_campaign_and_member(
        db,
        campaign_id,
        current_user.id
    )

    if status is not None and status not in VALID_STATUS:
        raise HTTPException(
            status_code=400,
            detail="Status không hợp lệ"
        )

    if priority is not None and priority not in VALID_PRIORITY:
        raise HTTPException(
            status_code=400,
            detail="Priority không hợp lệ"
        )

    query = (
        db.query(CampaignTask)
        .filter(
            CampaignTask.campaign_id == campaign_id
        )
    )

    if status:
        query = query.filter(
            CampaignTask.status == status
        )

    if priority:
        query = query.filter(
            CampaignTask.priority == priority
        )

    if assignee_id:
        query = query.filter(
            CampaignTask.assignee_id == assignee_id
        )

    if search:
        query = query.filter(
            CampaignTask.title.ilike(
                f"%{search.strip()}%"
            )
        )

    sort_column = CampaignTask.created_at

    if sort_by == "due_date":
        sort_column = CampaignTask.due_date

    if sort_order == "asc":
        query = query.order_by(
            sort_column.asc()
        )
    else:
        query = query.order_by(
            sort_column.desc()
        )

    return (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )


def get_campaign_task(
    db: Session,
    current_user: User,
    task_id: int
):
    task = (
        db.query(CampaignTask)
        .filter(CampaignTask.id == task_id)
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy công việc"
        )

    get_campaign_and_member(
        db,
        task.campaign_id,
        current_user.id
    )

    return task


def update_campaign_task(
    db: Session,
    current_user: User,
    task_id: int,
    title: str,
    description: str,
    due_date,
    status: str,
    priority: str,
    assignee_id: int
):
    task = get_campaign_task(
        db,
        current_user,
        task_id
    )

    campaign = (
        db.query(Campaign)
        .filter(
            Campaign.id == task.campaign_id
        )
        .first()
    )

    if (
        campaign.owner_id != current_user.id
        and task.assignee_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="Bạn không có quyền cập nhật công việc"
        )

    if not title or not title.strip():
        raise HTTPException(
            status_code=400,
            detail="Tên công việc không được để trống"
        )

    if status not in VALID_STATUS:
        raise HTTPException(
            status_code=400,
            detail="Status không hợp lệ"
        )

    if priority not in VALID_PRIORITY:
        raise HTTPException(
            status_code=400,
            detail="Priority không hợp lệ"
        )

    validate_assignee(
        db,
        task.campaign_id,
        assignee_id
    )

    task.title = title.strip()
    task.description = description
    task.due_date = due_date
    task.status = status
    task.priority = priority
    task.assignee_id = assignee_id

    db.commit()
    db.refresh(task)

    return task


def delete_campaign_task(
    db: Session,
    current_user: User,
    task_id: int
):
    task = get_campaign_task(
        db,
        current_user,
        task_id
    )

    campaign = (
        db.query(Campaign)
        .filter(
            Campaign.id == task.campaign_id
        )
        .first()
    )

    if campaign.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Chỉ OWNER mới được xóa công việc"
        )

    db.delete(task)
    db.commit()

    return {
        "message": "Xóa công việc thành công"
    }