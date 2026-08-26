from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.users import User
from app.schemas.users import UserResponse
from app.dependencies.auth import get_current_user, require_admin


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user


@router.get("", response_model=list[UserResponse])
def get_users(
    name: str = None,
    email: str = None,
    is_active: bool = None,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    query = db.query(User)

    if name:
        query = query.filter(
            User.full_name.contains(name)
        )

    if email:
        query = query.filter(
            User.email.contains(email)
        )

    if is_active is not None:
        query = query.filter(
            User.is_active == is_active
        )

    return query.all()