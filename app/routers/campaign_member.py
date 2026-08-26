from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.users import User
from app.schemas.campaign_member import (
    CampaignMemberCreate,
    CampaignMemberResponse
)
from app.services.campaign_member import (
    add_campaign_member,
    delete_campaign_member,
    get_campaign_members
)


router = APIRouter(
    prefix="/campaigns",
    tags=["Campaign Members"]
)


@router.post(
    "/{campaign_id}/members",
    response_model=CampaignMemberResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Thêm thành viên vào chiến dịch"
)
def add_member(
    campaign_id: int,
    member: CampaignMemberCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return add_campaign_member(
        db,
        current_user,
        campaign_id,
        member.user_id,
        member.position
    )


@router.delete(
    "/{campaign_id}/members/{user_id}"
)
def delete_member(
    campaign_id: int,
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return delete_campaign_member(
        db,
        current_user,
        campaign_id,
        user_id
    )


@router.get(
    "/{campaign_id}/members",
    response_model=list[CampaignMemberResponse]
)
def get_members(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_campaign_members(
        db,
        current_user,
        campaign_id
    )