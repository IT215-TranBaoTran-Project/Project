from datetime import datetime

from pydantic import BaseModel,ConfigDict,Field


class CampaignBase(BaseModel):
    name: str = Field(min_length=1,max_length=255)
    description: str | None = None


class CampaignCreate(CampaignBase):
    pass


class CampaignUpdate(CampaignBase):
    pass


class CampaignResponse(CampaignBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class CampaignMemberBase(BaseModel):
    campaign_id: int
    user_id: int
    role: str


class CampaignMemberCreate(BaseModel):
    user_id: int


class CampaignMemberUpdate(BaseModel):
    role: str


class CampaignMemberResponse(CampaignMemberBase):
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CampaignTaskBase(BaseModel):
    title: str = Field(min_length=1,max_length=255)
    description: str | None = None
    due_date: datetime | None = None
    priority: str

class CampaignTaskCreate(CampaignTaskBase):
    campaign_id: int


class CampaignTaskUpdate(CampaignTaskBase):
    pass


class CampaignTaskResponse(CampaignTaskBase):
    id: int
    campaign_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)