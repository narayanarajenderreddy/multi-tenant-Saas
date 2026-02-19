from sqlalchemy.orm import Session
from app.models.project import Project
from app.models.user import User
from fastapi import  HTTPException
from app.schemas.project import  ProjectCreate,ProjectResponse


def get_projects(
    db: Session,
    current_user: User,
    page: int,
    size: int,
    sort_by: str,
    order: str
):
    query = db.query(Project).filter(
        Project.is_deleted == False
    )

    if not current_user.is_super_admin:
        query = query.filter(
            Project.tenant_id == current_user.tenant_id
        )

    if hasattr(Project, sort_by):
        column = getattr(Project, sort_by)
        if order.lower() == "desc":
            query = query.order_by(column.desc())
        else:
            query = query.order_by(column.asc())

    total = query.count()
    offset = (page - 1) * size
    projects = query.offset(offset).limit(size).all()

    return {
        "total": total,
        "page": page,
        "size": size,
        "data": projects
    }
    


def create_project(db:Session,projectdata:ProjectCreate,current_user:User):
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

def delete_project(db:Session,project_id:int,current_user:User):
    if current_user.is_super_admin:
        project = db.query(Project).filter(Project.id == project_id,Project.is_deleted == False).first()
    else:    
        project = db.query(Project).filter(Project.tenant_id == current_user.tenant_id,Project.id == project_id,Project.is_deleted == False).first()
    if not project:
        raise HTTPException(status_code = 404,detail = "project not found")
    
    project.is_deleted = True
    db.commit()
    return{"message":"project has been deleted successfully"}
        
