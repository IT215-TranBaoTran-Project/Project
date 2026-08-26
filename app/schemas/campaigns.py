from datetime import datetime
from pydantic import BaseModel,ConfigDict,Field,field_validator


class CampaignBase(BaseModel):
    name: str = Field(min_length=1,max_length=255)
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
    title: str = Field(min_length=1,max_length=255)
    description: str
    due_date: datetime
    status: str
    priority: str
    assignee_id: int 

    @field_validator("status")
    @classmethod
    def validate_status(cls,value):
        if value not in ["TODO","IN_PROGRESS","DONE"]:
            raise ValueError("Status phải là TODO, IN_PROGRESS hoặc DONE")
        return value

    @field_validator("priority")
    @classmethod
    def validate_priority(cls,value):
        if value not in ["LOW","MEDIUM","HIGH"]:
            raise ValueError("Priority phải là LOW, MEDIUM hoặc HIGH")
        return value


class CampaignTaskCreate(BaseModel):
    title: str = Field(min_length=1,max_length=255)
    description: str
    due_date: datetime
    priority: str
    assignee_id: int 

    @field_validator("priority")
    @classmethod
    def validate_priority(cls,value):
        if value not in ["LOW","MEDIUM","HIGH"]:
            raise ValueError("Priority phải là LOW, MEDIUM hoặc HIGH")
        return value


class CampaignTaskUpdate(BaseModel):
    title: str 
    description: str 
    due_date: datetime 
    status: str 
    priority: str 
    assignee_id: int 

    @field_validator("status")
    @classmethod
    def validate_status(cls,value):
        if value is not None and value not in ["TODO","IN_PROGRESS","DONE"]:
            raise ValueError("Status phải là TODO, IN_PROGRESS hoặc DONE")
        return value

    @field_validator("priority")
    @classmethod
    def validate_priority(cls,value):
        if value is not None and value not in ["LOW","MEDIUM","HIGH"]:
            raise ValueError("Priority phải là LOW, MEDIUM hoặc HIGH")
        return value


class CampaignTaskResponse(CampaignTaskBase):
    id: int
    campaign_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)