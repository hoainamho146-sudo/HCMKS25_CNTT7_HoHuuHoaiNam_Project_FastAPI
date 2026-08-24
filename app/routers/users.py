from fastapi import APIRouter, Depends, Query
from app.core.dependencies import get_current_user, RoleChecker
from app.models.user import User
from app.schemas.user import UserResponse
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.db.database import get_db

router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("", response_model=List[UserResponse])
def get_users(
    search: str = Query(None, description="Tìm kiếm theo tên hoặc email"),
    is_active: bool = Query(None, description="Lọc theo trạng thái hoạt động"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(RoleChecker(["ADMIN"]))
):
    
    query = db.query(User)

    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                User.full_name.ilike(search_pattern),
                User.email.ilike(search_pattern)
            )
        )

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    return query.all()