from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class CampaignBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str


class CampaignCreate(CampaignBase):
    pass


class CampaignUpdate(CampaignBase):
    pass


class CampaignResponse(CampaignBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CampaignMemberBase(BaseModel):
    campaign_id: int
    user_id: int
    role: str
    position: str


class CampaignMemberCreate(BaseModel):
    user_id: int
    position: str


class CampaignMemberUpdate(BaseModel):
    role: str
    position: str


class CampaignMemberResponse(CampaignMemberBase):
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CampaignTaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str
    due_date: datetime
    priority: str
    assignee_id: int | None = None


class CampaignTaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str
    due_date: datetime
    priority: str
    assignee_id: int | None = None


class CampaignTaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    due_date: datetime | None = None
    priority: str | None = None
    assignee_id: int | None = None


class CampaignTaskResponse(CampaignTaskBase):
    id: int
    campaign_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)