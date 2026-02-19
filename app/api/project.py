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
    if  current_user.role != "admin":
        raise HTTPException(status_code=400,detail="You have no access to create project")
    
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
    if current_user.is_super_admin:
        return db.query(Project).all()
    if current_user.role == "admin":
        return db.query(Project).filter(Project.tenant_id == current_user.tenant_id).all()
    
@router.post("/project_delete/{project_id}")
def delete_project(project_id:int,db:Session = Depends(get_db),current_user:User = Depends(get_current_user)):
    if current_user.is_super_admin:
        project = db.query(Project).filter(Project.id == project_id,Project.is_deleted == False).first()
    else:    
        project = db.query(Project).filter(Project.tenant_id == current_user.tenant_id,Project.id == project_id,Project.is_deleted == False).first()
    if not project:
        raise HTTPException(status_code = 404,detail = "project not found")
    
    project.is_deleted = True
    db.commit()
    return{"message":"project has been deleted successfully"}
    
    
    
    
        
    
