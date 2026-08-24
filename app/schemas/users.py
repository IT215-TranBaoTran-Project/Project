from datetime import datetime

from pydantic import BaseModel,ConfigDict,EmailStr,Field,field_validator


class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=1,max_length=255)


class UserCreate(UserBase):
    password: str = Field(min_length=6,max_length=72)

    @field_validator("password")
    @classmethod
    def validate_password_length(cls,value: str):
        if len(value.encode("utf-8")) > 72:
            raise ValueError("Mật khẩu không được vượt quá 72 bytes")
        return value


class UserUpdate(BaseModel):
    full_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255
    )

    is_active: bool | None = None


class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"