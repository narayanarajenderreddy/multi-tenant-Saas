from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from fastapi import Query
from typing import Optional
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectResponse
from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.services.project_service import get_projects


router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/create_project",response_model=ProjectResponse)
def create_project(projectdata:ProjectCreate,db:Session = Depends(get_db),current_user:User = Depends(get_current_user)):
    return create_project(db,projectdata,current_user)
    
@router.get("/list_project",response_model= List[ProjectResponse])
def project_list(db:Session = Depends(get_db),current_user:User = Depends(get_current_user),
                 page:int = Query(1,ge=1),
                 size:int = Query(10,ge=1,le=100),
                 sort_by:Optional[str] = "created_at",
                 order:Optional[str] = "desc"):
    return get_projects(db,current_user,page,size,sort_by,order)
    
    
@router.post("/project_delete/{project_id}")
def delete_project(project_id:int,db:Session = Depends(get_db),current_user:User = Depends(get_current_user)):
    return delete_project(db,project_id,current_user)
    
    
    
    
    
        
    
