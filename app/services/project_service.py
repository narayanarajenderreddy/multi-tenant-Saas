from sqlalchemy.orm import Session
from app.models.project import Project
from app.models.user import User
from fastapi import  HTTPException
from app.schemas.project import  ProjectCreate,ProjectResponse
from app.core.response import pagination_response,success_response
import json
from  app.core.redis_client import redis_client


# def get_projects(
#     db: Session,
#     current_user: User,
#     page: int,
#     size: int,
#     sort_by: str,
#     order: str
# ):
#     query = db.query(Project).filter(
#         Project.is_deleted == True
#     )
    

#     if not current_user.is_super_admin:
#         query = query.filter(
#             Project.tenant_id == current_user.tenant_id
#         )

#     if hasattr(Project, sort_by):
#         column = getattr(Project, sort_by)
#         if order.lower() == "desc":
#             query = query.order_by(column.desc())
#         else:
#             query = query.order_by(column.asc())

#     total = query.count()
#     offset = (page - 1) * size
#     projects = query.offset(offset).limit(size).all()

#     return pagination_response(
#         items=projects,
#         page=page,
#         size=size,
#         total=total
#     )
    


def create_new_project(db:Session,projectdata:ProjectCreate,current_user:User):
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
    
    return success_response(data=add_new_project)

def delete_project_list(db:Session,project_id:int,current_user:User):
    if current_user.is_super_admin:
        project = db.query(Project).filter(Project.id == project_id,Project.is_deleted == False).first()
    else:    
        project = db.query(Project).filter(Project.tenant_id == current_user.tenant_id,Project.id == project_id,Project.is_deleted == False).first()
    if not project:
        raise HTTPException(status_code = 404,detail = "project not found")
    
    project.is_deleted = True
    db.commit()
    return success_response(message="project has been deleted successfully")


def get_projects(db:Session,current_user:User,page:int,size:int,sort_by:str,order:str):
    cache_key = f"projects:{current_user.tenant_id}:{page}:{size}:{sort_by}:{order}"
    cached_result = redis_client.get(cache_key)
    if cached_result:
        print("cache hit")
        return json.loads(cached_result)
    print("cache miss")
    
    query = db.query(Project).filter(Project.is_deleted == False)

    if not current_user.is_super_admin:
        query = query.filter(Project.tenant_id == current_user.tenant_id)
    total = query.count()
    
    if hasattr(Project,sort_by):
        column = getattr(Project,sort_by)
        query = query.order_by(column.desc() if order == "desc" else column.asc())

    offset = (page - 1) * size
    projects = query.offset(offset).limit(size).all()

    result = {
        "items": [p.id for p in projects],  # simplify for now
        "page": page,
        "size": size,
        "total": total
    }

    # 🟢 STEP 2 — Store in cache (TTL 60 sec)
    redis_client.setex(cache_key, 60, json.dumps(result))

    return result        