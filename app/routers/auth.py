from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.users import UserCreate, UserResponse, LoginRequest, TokenResponse
from app.services.auth import register_user, login_user
from jose import jwt, JWTError

from app.core.security import (
    SECRET_KEY,
    ALGORITHM,
    create_access_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

login_attempts = {}

@router.post("/register", response_model=UserResponse)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return register_user(db, user)

@router.post("/login", response_model=TokenResponse)
def login(
    user: LoginRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    ip = request.client.host

    if ip not in login_attempts:
        login_attempts[ip] = {
            "count": 0
        }

    if login_attempts[ip]["count"] >= 5:
        raise HTTPException(
            status_code=429,
            detail="Bạn đăng nhập sai quá nhiều lần, vui lòng thử lại sau"
        )

    try:
        result = login_user(db, user)

        login_attempts[ip]["count"] = 0

        return result

    except HTTPException as e:
        if e.status_code == 401:
            login_attempts[ip]["count"] += 1

        raise e


@router.post("/refresh")
def refresh_token(
    refresh_token: str
):
    try:
        payload = jwt.decode(
            refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=401,
                detail="Refresh token không hợp lệ"
            )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Refresh token không hợp lệ"
            )

        access_token = create_access_token({
            "sub": user_id
        })

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Refresh token không hợp lệ hoặc đã hết hạn"
        )