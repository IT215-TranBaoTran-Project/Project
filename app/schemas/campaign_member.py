from pydantic import BaseModel, ConfigDict
from datetime import datetime


class CampaignMemberCreate(BaseModel):
    user_id: int
    position: str


class CampaignMemberResponse(BaseModel):
    campaign_id: int
    user_id: int
    role: str
    position: str
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)