from fastapi import FastAPI
from app.db.database import Base, engine
from app.models import user, project, project_members, task

app = FastAPI(
    title="Project Management API",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Khởi tạo thành công"}