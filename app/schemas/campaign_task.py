from pydantic import BaseModel, ConfigDict
from datetime import datetime


class CampaignTaskBase(BaseModel):
    title: str
    description: str
    status: str
    pririty: str
    due_date: datetime


class CampaignTaskCreate(CampaignTaskBase):
    campaign_id: int
    assignee_id: int


class CampaignTaskUpdate(CampaignTaskBase):
    pass


class CampaignTaskResponse(CampaignTaskBase):
    id: int
    campaign_id: int
    assignee_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)