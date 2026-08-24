from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.project import Project
from app.models.project_members import ProjectMember
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.schemas.project_members import ProjectMemberCreate

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

def check_project_owner(db: Session, project_id: int, user_id: int) -> Project:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dự án không tồn tại"
        )
    
    is_owner = (
        project.owner_id == user_id
        or db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == user_id,
            ProjectMember.role == "OWNER"
        )
        .first()
    )
    
    if not is_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Quyền bị từ chối! Chỉ OWNER của dự án mới được thực hiện thao tác này"
        )
    return project

def update_project(db: Session, project_id: int, update_data: ProjectUpdate, user_id: int) -> Project:
    project = check_project_owner(db=db, project_id=project_id, user_id=user_id)
    
    data_dict = update_data.model_dump(exclude_unset=True)
    for field, value in data_dict.items():
        setattr(project, field, value)
        
    db.commit()
    db.refresh(project)
    return project

def delete_project(db: Session, project_id: int, user_id: int) -> None:
    project = check_project_owner(db=db, project_id=project_id, user_id=user_id)
    
    db.delete(project)
    db.commit()

def add_member_to_project(
    db: Session, project_id: int, member_data: ProjectMemberCreate, current_user_id: int
) -> ProjectMember:
    check_project_owner(db=db, project_id=project_id, user_id=current_user_id)

    target_user = db.query(User).filter(User.id == member_data.user_id).first()
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Người dùng được thêm không tồn tại"
        )

    existing_member = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == member_data.user_id
        )
        .first()
    )
    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Người dùng này đã là thành viên của dự án"
        )

    new_member = ProjectMember(
        project_id=project_id,
        user_id=member_data.user_id,
        role=member_data.role.upper()
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    return new_member