from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectResponse
from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/create_project",response_model=ProjectResponse)
def create_project(projectdata:ProjectCreate,db:Session = Depends(get_db),current_user:User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=400,
                            message = "Invalid credentials")
    add_new_project =   Project(
        name = projectdata.name,
        description = projectdata.description,
        created_by = current_user.id,
        tenant_id = current_user.tenant_id
        
    )  
    
    db.add(add_new_project)
    db.commit()
    db.refresh(add_new_project)
    
    return add_new_project

@router.get("/list_project",response_model= List[ProjectResponse])
def project_list(db:Session = Depends(get_db),current_user:User = Depends(get_current_user)):
    project_list = db.query(Project).filter(Project.tenant_id == current_user.tenant_id).all()
    return project_list