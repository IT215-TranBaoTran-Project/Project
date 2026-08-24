from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.db.database import get_db
from app.models.users import User
from app.models.campaigns import Campaign, CampaignMember
from app.schemas.campaigns import (
    CampaignCreate,
    CampaignUpdate,
    CampaignResponse
)
from app.dependencies.auth import get_current_user


router = APIRouter(
    prefix="/campaigns",
    tags=["Campaigns"]
)

@router.post("", response_model=CampaignResponse)
def create_campaign(
    campaign: CampaignCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_campaign = Campaign(
        name=campaign.name,
        description=campaign.description,
        owner_id=current_user.id
    )

    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)

    new_member = CampaignMember(
        campaign_id=new_campaign.id,
        users_id=current_user.id,
        role="OWNER"
    )

    db.add(new_member)
    db.commit()

    return new_campaign


@router.get("", response_model=list[CampaignResponse])
def get_campaigns(
    search: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    campaigns = db.query(Campaign).join(
        CampaignMember,
        Campaign.id == CampaignMember.campaign_id,
        isouter=True
    ).filter(
        or_(
            Campaign.owner_id == current_user.id,
            CampaignMember.users_id == current_user.id
        )
    )

    if search:
        campaigns = campaigns.filter(
            Campaign.name.ilike(f"%{search}%")
        )

    return campaigns.distinct().all()


@router.get("/{campaign_id}", response_model=CampaignResponse)
def get_campaign(
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
        CampaignMember.users_id == current_user.id
    ).first()

    if member is None:
        raise HTTPException(
            status_code=403,
            detail="Bạn không phải thành viên của chiến dịch"
        )

    return campaign


@router.put("/{campaign_id}", response_model=CampaignResponse)
def update_campaign(
    campaign_id: int,
    campaign: CampaignUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    campaign_db = db.query(Campaign).filter(
        Campaign.id == campaign_id
    ).first()

    if campaign_db is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy chiến dịch"
        )

    if campaign_db.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Chỉ OWNER mới được sửa chiến dịch"
        )

    if campaign.name is not None:
        campaign_db.name = campaign.name

    if campaign.description is not None:
        campaign_db.description = campaign.description

    db.commit()
    db.refresh(campaign_db)

    return campaign_db


@router.patch("/{campaign_id}", response_model=CampaignResponse)
def patch_campaign(
    campaign_id: int,
    campaign: CampaignUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    campaign_db = db.query(Campaign).filter(
        Campaign.id == campaign_id
    ).first()

    if campaign_db is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy chiến dịch"
        )

    if campaign_db.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Chỉ OWNER mới được sửa chiến dịch"
        )

    if campaign.name is not None:
        campaign_db.name = campaign.name

    if campaign.description is not None:
        campaign_db.description = campaign.description

    db.commit()
    db.refresh(campaign_db)

    return campaign_db


@router.delete("/{campaign_id}")
def delete_campaign(
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