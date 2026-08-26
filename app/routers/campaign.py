from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.users import User
from app.schemas.campaigns import (
    CampaignCreate,
    CampaignResponse,
    CampaignUpdate
)
from app.services.campaign import (
    create_campaign,
    get_campaigns,
    get_campaign_by_id,
    update_campaign,
    delete_campaign
)


router = APIRouter(
    prefix="/campaigns",
    tags=["Campaigns"]
)


@router.post(
    "",
    response_model=CampaignResponse
)
def create_campaign_endpoint(
    campaign: CampaignCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_campaign(
        db,
        current_user,
        campaign.name,
        campaign.description
    )


@router.get(
    "",
    response_model=list[CampaignResponse]
)
def get_campaigns_endpoint(
    search: str | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_campaigns(
        db,
        current_user,
        search
    )


@router.get(
    "/{campaign_id}",
    response_model=CampaignResponse
)
def get_campaign_by_id_endpoint(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_campaign_by_id(
        db,
        current_user,
        campaign_id
    )


@router.put(
    "/{campaign_id}",
    response_model=CampaignResponse
)
def update_campaign_endpoint(
    campaign_id: int,
    campaign: CampaignUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return update_campaign(
        db,
        current_user,
        campaign_id,
        campaign.name,
        campaign.description
    )


@router.delete(
    "/{campaign_id}"
)
def delete_campaign_endpoint(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return delete_campaign(
        db,
        current_user,
        campaign_id
    )