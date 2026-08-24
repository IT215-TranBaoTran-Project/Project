from datetime import datetime

from pydantic import BaseModel,ConfigDict,EmailStr,Field


class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=1,max_length=255)


class UserCreate(UserBase):
    password: str = Field(min_length=6,max_length=100)


class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None,min_length=1,max_length=255)
    is_active: bool | None = None


class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)