from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from app.services import project_service

router = APIRouter(
    prefix="/api/projects",
    tags=["Projects"]
)

@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_new_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return project_service.create_project(
        db=db, 
        project_data=project_data, 
        user_id=current_user.id
    )

@router.get("", response_model=list[ProjectResponse], status_code=status.HTTP_200_OK)
def list_projects(
    search: str | None = Query(None, description="Tìm kiếm theo tên dự án"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return project_service.get_user_projects(
        db=db,
        user_id=current_user.id,
        search=search
    )

@router.get("/{project_id}", response_model=ProjectResponse, status_code=status.HTTP_200_OK)
def get_project_detail(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return project_service.get_project_by_id(
        db=db,
        project_id=project_id,
        user_id=current_user.id
    )

@router.put("/{project_id}", response_model=ProjectResponse, status_code=status.HTTP_200_OK)
@router.patch("/{project_id}", response_model=ProjectResponse, status_code=status.HTTP_200_OK)
def update_existing_project(
    project_id: int,
    update_data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return project_service.update_project(
        db=db,
        project_id=project_id,
        update_data=update_data,
        user_id=current_user.id
    )

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project_service.delete_project(
        db=db,
        project_id=project_id,
        user_id=current_user.id
    )
    return None