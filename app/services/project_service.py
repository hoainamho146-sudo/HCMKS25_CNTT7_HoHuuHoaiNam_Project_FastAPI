from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.project import Project
from app.models.project_members import ProjectMember
from app.schemas.project import ProjectCreate

def create_project(db: Session, project_data: ProjectCreate, user_id: int) -> Project:
    new_project = Project(
        name=project_data.name,
        description=project_data.description,
        owner_id=user_id
    )
    db.add(new_project)
    db.flush()

    new_member = ProjectMember(
        project_id=new_project.id,
        user_id=user_id,
        role="OWNER"
    )
    db.add(new_member)
    
    db.commit()
    db.refresh(new_project)
    
    return new_project

def get_user_projects(db: Session, user_id: int, search: str | None = None) -> list[Project]:
    query = (
        db.query(Project)
        .join(ProjectMember, Project.id == ProjectMember.project_id)
        .filter(ProjectMember.user_id == user_id)
    )

    if search:
        query = query.filter(Project.name.ilike(f"%{search.strip()}%"))

    return query.distinct().all()

def get_project_by_id(db: Session, project_id: int, user_id: int) -> Project:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dự án không tồn tại"
        )

    is_member = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == user_id
        )
        .first()
    )

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Quyền truy cập bị từ chối! Bạn không phải là thành viên của dự án này"
        )

    return project