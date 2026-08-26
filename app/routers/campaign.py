from fastapi import APIRouter, Depends, HTTPException, status

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


@router.post(
    "",
    response_model=CampaignResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Tạo chiến dịch",
    description=(
        "Tạo một chiến dịch mới. Người dùng đăng nhập sẽ trở thành "
        "OWNER của chiến dịch và được thêm tự động vào danh sách thành viên."
    ),
    response_description="Thông tin chiến dịch vừa được tạo."
)
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
        user_id=current_user.id,
        role="OWNER",
        position="CONTENT"
    )

    db.add(new_member)
    db.commit()

    return new_campaign


@router.get(
    "",
    response_model=list[CampaignResponse],
    status_code=status.HTTP_200_OK,
    summary="Lấy danh sách chiến dịch",
    description=(
        "Lấy danh sách các chiến dịch mà người dùng hiện tại là OWNER "
        "hoặc thành viên. Có thể tìm kiếm chiến dịch theo tên."
    ),
    response_description="Danh sách chiến dịch mà người dùng có quyền truy cập."
)
def get_campaigns(
    search: str | None = None,
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
            CampaignMember.user_id == current_user.id
        )
    )

    if search:
        campaigns = campaigns.filter(
            Campaign.name.ilike(f"%{search}%")
        )

    return campaigns.distinct().all()


@router.get(
    "/{campaign_id}",
    response_model=CampaignResponse,
    status_code=status.HTTP_200_OK,
    summary="Lấy thông tin chiến dịch",
    description=(
        "Lấy thông tin chi tiết của một chiến dịch. "
        "Chỉ OWNER hoặc thành viên của chiến dịch mới được truy cập."
    ),
    response_description="Thông tin chi tiết của chiến dịch."
)
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
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy chiến dịch"
        )

    member = db.query(CampaignMember).filter(
        CampaignMember.campaign_id == campaign_id,
        CampaignMember.user_id == current_user.id
    ).first()

    if campaign.owner_id != current_user.id and member is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không phải thành viên của chiến dịch"
        )

    return campaign


@router.put(
    "/{campaign_id}",
    response_model=CampaignResponse,
    status_code=status.HTTP_200_OK,
    summary="Cập nhật chiến dịch",
    description=(
        "Cập nhật thông tin chiến dịch. "
        "Chỉ OWNER của chiến dịch mới có quyền thực hiện."
    ),
    response_description="Thông tin chiến dịch sau khi cập nhật."
)
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
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy chiến dịch"
        )

    if campaign_db.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ OWNER mới được sửa chiến dịch"
        )

    if campaign.name is not None:
        campaign_db.name = campaign.name

    if campaign.description is not None:
        campaign_db.description = campaign.description

    db.commit()
    db.refresh(campaign_db)

    return campaign_db


@router.patch(
    "/{campaign_id}",
    response_model=CampaignResponse,
    status_code=status.HTTP_200_OK,
    summary="Cập nhật một phần chiến dịch",
    description=(
        "Cập nhật một hoặc nhiều trường của chiến dịch. "
        "Các trường không gửi lên sẽ được giữ nguyên. "
        "Chỉ OWNER mới có quyền cập nhật."
    ),
    response_description="Thông tin chiến dịch sau khi cập nhật."
)
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
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy chiến dịch"
        )

    if campaign_db.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ OWNER mới được sửa chiến dịch"
        )

    if campaign.name is not None:
        campaign_db.name = campaign.name

    if campaign.description is not None:
        campaign_db.description = campaign.description

    db.commit()
    db.refresh(campaign_db)

    return campaign_db


@router.delete(
    "/{campaign_id}",
    status_code=status.HTTP_200_OK,
    summary="Xóa chiến dịch",
    description=(
        "Xóa một chiến dịch. "
        "Chỉ OWNER của chiến dịch mới có quyền xóa."
    ),
    response_description="Thông báo xóa chiến dịch thành công."
)
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
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy chiến dịch"
        )

    if campaign.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ OWNER mới được xóa chiến dịch"
        )

    db.delete(campaign)
    db.commit()

    return {
        "message": "Xóa chiến dịch thành công"
    }