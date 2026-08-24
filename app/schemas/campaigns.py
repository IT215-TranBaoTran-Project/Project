from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class CampaignCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=255
    )
    description: str 


class CampaignUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1,max_length=255)
    description: str 

class CampaignResponse(BaseModel):
    id: int
    name: str
    description: str 
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)