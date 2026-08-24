from pydantic import BaseModel, ConfigDict
from datetime import datetime


class CampaignMemberCreate(BaseModel):
    users_id: int


class CampaignMemberResponse(BaseModel):
    campaign_id: int
    users_id: int
    role: str
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)