from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.users import User
from app.models.campaigns import Campaign, CampaignMember


VALID_POSITIONS = [
    "CONTENT",
    "ADS",
    "DESIGN"
]


def add_campaign_member(
    db: Session,
    current_user: User,
    campaign_id: int,
    user_id: int,
    position: str
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

    if campaign.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Chỉ OWNER mới được thêm thành viên"
        )

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy người dùng"
        )

    if position not in VALID_POSITIONS:
        raise HTTPException(
            status_code=400,
            detail="Position phải là CONTENT, ADS hoặc DESIGN"
        )

    existing_member = (
        db.query(CampaignMember)
        .filter(
            CampaignMember.campaign_id == campaign_id,
            CampaignMember.user_id == user_id
        )
        .first()
    )

    if existing_member is not None:
        raise HTTPException(
            status_code=400,
            detail="Người dùng đã là thành viên"
        )

    member = CampaignMember(
        campaign_id=campaign_id,
        user_id=user_id,
        role="MEMBER",
        position=position
    )

    db.add(member)
    db.commit()
    db.refresh(member)

    return member


def delete_campaign_member(
    db: Session,
    current_user: User,
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

    if campaign.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Chỉ OWNER mới được xóa thành viên"
        )

    member = (
        db.query(CampaignMember)
        .filter(
            CampaignMember.campaign_id == campaign_id,
            CampaignMember.user_id == user_id
        )
        .first()
    )

    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Người dùng không phải thành viên"
        )

    if member.role == "OWNER":
        owner_count = (
            db.query(CampaignMember)
            .filter(
                CampaignMember.campaign_id == campaign_id,
                CampaignMember.role == "OWNER"
            )
            .count()
        )

        if owner_count <= 1:
            raise HTTPException(
                status_code=400,
                detail="Không thể xóa OWNER cuối cùng"
            )

    db.delete(member)
    db.commit()

    return {
        "message": "Xóa thành viên thành công"
    }


def get_campaign_members(
    db: Session,
    current_user: User,
    campaign_id: int
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
            CampaignMember.user_id == current_user.id
        )
        .first()
    )

    if (
        campaign.owner_id != current_user.id
        and member is None
    ):
        raise HTTPException(
            status_code=403,
            detail="Bạn không phải thành viên của chiến dịch"
        )

    return (
        db.query(CampaignMember)
        .filter(
            CampaignMember.campaign_id == campaign_id
        )
        .all()
    )