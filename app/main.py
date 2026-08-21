from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.database import Base, engine, get_db
from app.models import user, project, project_members, task
from app.core.exceptions import AppException, app_exception_handler
from app.routers import auth

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Project Management API",
    version="1.0.0"
)

app.add_exception_handler(AppException, app_exception_handler)

@app.get("/")
def root():
    return {"message": "Khởi tạo thành công"}

@app.get("/health", status_code=status.HTTP_200_OK, tags=["Health Check"])
def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint: Kiểm tra trạng thái hoạt động của API và kết nối Database.
    """
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": f"disconnected: {str(e)}"
        }