from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.users import User
from app.models.campaigns import Campaign, CampaignMember

from app.schemas.campaign_member import (
    CampaignMemberCreate,
    CampaignMemberResponse
)

from app.dependencies.auth import get_current_user


router = APIRouter(
    prefix="/campaigns",
    tags=["Campaign Members"]
)


@router.post(
    "/{campaign_id}/members",
    response_model=CampaignMemberResponse
)
def add_member(
    campaign_id: int,
    member: CampaignMemberCreate,
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

    if campaign.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Chỉ OWNER mới được thêm thành viên"
        )

    user = db.query(User).filter(
        User.id == member.user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy người dùng"
        )

    existing_member = db.query(CampaignMember).filter(
        CampaignMember.campaign_id == campaign_id,
        CampaignMember.user_id == member.user_id
    ).first()

    if existing_member:
        raise HTTPException(
            status_code=400,
            detail="Người dùng đã là thành viên của chiến dịch"
        )

    if member.position not in [
        "CONTENT",
        "ADS",
        "DESIGN"
    ]:
        raise HTTPException(
            status_code=400,
            detail="Position phải là CONTENT, ADS hoặc DESIGN"
        )

    new_member = CampaignMember(
        campaign_id=campaign_id,
        user_id=member.user_id,
        role="MEMBER",
        position=member.position
    )

    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    return new_member


@router.delete(
    "/{campaign_id}/members/{user_id}"
)
def delete_member(
    campaign_id: int,
    user_id: int,
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

    if campaign.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Chỉ OWNER mới được xóa thành viên"
        )

    member = db.query(CampaignMember).filter(
        CampaignMember.campaign_id == campaign_id,
        CampaignMember.user_id == user_id
    ).first()

    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Người dùng không phải thành viên của chiến dịch"
        )

    if member.role == "OWNER":
        owner_count = db.query(CampaignMember).filter(
            CampaignMember.campaign_id == campaign_id,
            CampaignMember.role == "OWNER"
        ).count()

        if owner_count == 1:
            raise HTTPException(
                status_code=400,
                detail="Không thể xóa OWNER cuối cùng"
            )

    db.delete(member)
    db.commit()

    return {
        "message": "Xóa thành viên thành công"
    }


@router.get(
    "/{campaign_id}/members"
)
def get_members(
    campaign_id: int,
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

    members = db.query(CampaignMember).filter(
        CampaignMember.campaign_id == campaign_id
    ).all()

    return members