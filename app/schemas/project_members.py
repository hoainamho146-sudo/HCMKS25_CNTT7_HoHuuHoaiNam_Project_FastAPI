from datetime import datetime
from pydantic import BaseModel

class ProjectMemberBase(BaseModel):
    role: str

class ProjectMemberCreate(ProjectMemberBase):
    project_id: int
    user_id: int

class ProjectMemberUpdate(BaseModel):
    role: str | None = None

class ProjectMemberResponse(ProjectMemberBase):
    project_id: int
    user_id: int
    joined_at: datetime

    class Config:
        from_attributes = True