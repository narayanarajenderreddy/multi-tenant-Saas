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
from app.services.project_service import get_projects,delete_project_list,create_new_project
from app.core.response import success_response
from fastapi import Request
from app.core.roles import Roles
from app.core.permissions import Permissions
from app.core.dependencies import require_roles,require_permission,require_role_and_permission


router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/create_project")
def create_project(projectdata:ProjectCreate,db:Session = Depends(get_db),current_user:User = Depends(require_roles([Roles.SUPER_ADMIN, Roles.ADMIN]))):
    result =  create_new_project(db,projectdata,current_user)
    return success_response(
        data = result,
        message = "project has been created successfuly."
    )
    
@router.get("/list_project")
def project_list(request: Request,db:Session = Depends(get_db),
                 current_user:User = Depends(require_role_and_permission([Roles.SUPER_ADMIN, Roles.ADMIN, Roles.MEMBER], Permissions.VIEW_PROJECT)),
                 page:int = Query(1,ge=1),
                 size:int = Query(10,ge=1,le=100),
                 sort_by:Optional[str] = "created_at",
                 order:Optional[str] = "desc"):
    print("Tenant from middleware:", request.state.tenant_id)
    result =  get_projects(db,current_user,page,size,sort_by,order)
    return success_response(
        data = result,
        message = "project list fetched sucessfully."
    )
    
    
@router.post("/project_delete/{project_id}")
def delete_project(project_id:int,db:Session = Depends(get_db),current_user:User = Depends(require_roles([Roles.SUPER_ADMIN, Roles.ADMIN]))):
    result =  delete_project_list(db,project_id,current_user)
    return success_response(
        data = result,
        message = "project has been  deleted successfully."
    )
    
    
    
    
    
        
    
