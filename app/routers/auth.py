from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordRequestForm

from app.db.database import get_db

from app.schemas.users import (
    UserCreate,
    UserResponse,
    LoginRequest,
    TokenResponse
)

from app.services.auth import (
    register_user,
    login_user
)


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post(
    "/register",
    response_model=UserResponse
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return register_user(
        db,
        user
    )


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return login_user(
        db,
        LoginRequest(
            email=form_data.username,
            password=form_data.password
        )
    )