from pydantic import BaseModel, ConfigDict
from datetime import datetime


class UserBase(BaseModel):
    email: str
    full_name: str
    role: str
    is_active: bool


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: str
    full_name: str
    role: str
    is_active: bool
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str