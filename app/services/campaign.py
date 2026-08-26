from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.campaigns import Campaign, CampaignMember
from app.models.users import User


def create_campaign(
    db: Session,
    current_user: User,
    name: str,
    description: str
):
    if not name or not name.strip():
        raise HTTPException(
            status_code=400,
            detail="Tên chiến dịch không được để trống"
        )

    if len(name.strip()) > 255:
        raise HTTPException(
            status_code=400,
            detail="Tên chiến dịch không được vượt quá 255 ký tự"
        )

    campaign = Campaign(
        name=name.strip(),
        description=description,
        owner_id=current_user.id
    )

    db.add(campaign)
    db.flush()

    owner = CampaignMember(
        campaign_id=campaign.id,
        user_id=current_user.id,
        role="OWNER",
        position="CONTENT"
    )

    db.add(owner)
    db.commit()
    db.refresh(campaign)

    return campaign


def get_campaigns(
    db: Session,
    current_user: User,
    search: str | None = None
):
    query = (
        db.query(Campaign)
        .join(
            CampaignMember,
            Campaign.id == CampaignMember.campaign_id,
            isouter=True
        )
        .filter(
            or_(
                Campaign.owner_id == current_user.id,
                CampaignMember.user_id == current_user.id
            )
        )
        .distinct()
    )

    if search and search.strip():
        query = query.filter(
            Campaign.name.ilike(
                f"%{search.strip()}%"
            )
        )

    return query.all()


def get_campaign_by_id(
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

    return campaign


def update_campaign(
    db: Session,
    current_user: User,
    campaign_id: int,
    name: str,
    description: str
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
            detail="Chỉ OWNER mới được sửa chiến dịch"
        )

    if not name or not name.strip():
        raise HTTPException(
            status_code=400,
            detail="Tên chiến dịch không được để trống"
        )

    if len(name.strip()) > 255:
        raise HTTPException(
            status_code=400,
            detail="Tên chiến dịch không được vượt quá 255 ký tự"
        )

    campaign.name = name.strip()
    campaign.description = description

    db.commit()
    db.refresh(campaign)

    return campaign


def delete_campaign(
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

    if campaign.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Chỉ OWNER mới được xóa chiến dịch"
        )

    db.delete(campaign)
    db.commit()

    return {
        "message": "Xóa chiến dịch thành công"
    }