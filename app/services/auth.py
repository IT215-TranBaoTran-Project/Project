from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.users import User
from app.schemas.users import UserCreate, LoginRequest
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token
)


def register_user(db: Session, user: UserCreate):
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    existing_user = db.query(User).filter( User.email == user.email).first()


    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email đã tồn tại"
        )

    new_user = User(
        email=user.email,
        password_hash=hash_password(user.password),
        full_name=user.full_name,
        role=user.role,
        is_active=user.is_active
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user(db: Session, user: LoginRequest):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Email hoặc mật khẩu không đúng"
        )

    if not verify_password(
        user.password,
        existing_user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Email hoặc mật khẩu không đúng"
        )

    if not existing_user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Tài khoản không hoạt động"
        )

    access_token = create_access_token({
        "sub": str(existing_user.id),
        "email": existing_user.email,
        "role": existing_user.role
    })

    refresh_token = create_refresh_token({
        "sub": str(existing_user.id)
    })

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }