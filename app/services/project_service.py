from sqlalchemy.orm import Session
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