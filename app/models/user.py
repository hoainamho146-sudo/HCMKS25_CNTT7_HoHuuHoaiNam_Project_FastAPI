from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), default = "USER")
    is_active = Column(Boolean, default = True)
    created_at = Column(DateTime, nullable=False)

    projects = relationship("Project", back_populates="owner")
    project_members = relationship("ProjectMember", back_populates="user")
    tasks = relationship("Task", back_populates="assignee")