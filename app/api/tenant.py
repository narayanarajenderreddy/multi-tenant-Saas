from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.user import User
from app.models.tenant import Tenant
from app.schemas.tenant import TenantCreate
from app.core.security import hash_password, verify_password, create_access_token
from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/tenant", tags=["Tenant"])

@router.post("/")
def create_tenant(payload:TenantCreate,db:Session = Depends(get_db),current_user:User = Depends(get_current_user)):
    if not current_user.is_super_admin:
        raise HTTPException(
            status_code=400,
            message = "You have no access to create tenant."
        )
    new_tenant =  Tenant(
        name = payload.name,
        subdomain = payload.subdomain,
        is_active = payload.is_active
        
    )
    
    db.add(new_tenant)
    db.commit()
    db.refresh(new_tenant)
    
    return { 
        "tenant_details":new_tenant,
        "message":"New tenant has been created successfully."
    }


@router.get("/tenant_List")
# def  tenantuserlist(db:Session = Depends(get_db),currentuser:User = Depends(get_current_user)):
#     userslist = db.query(User).filter(User.tenant_id == currentuser.tenant_id).first()
#     if not userslist:
#       raise HTTPException(
#           status_code=400,
#           message = "No users for current login tenant"
#       )
#     return userslist
def get_tenants(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.is_super_admin:
        return db.query(Tenant).all()

    return [current_user.tenant]

@router.get("/tenant_userlist")
# def tenant_userlist(db:Session=Depends(get_db),current_user:User = Depends(get_current_user)):
#     if not current_user.tenant_id:
#         raise HTTPException(status_code = 400,
#                             detail = "something went wrong")
       
#     tenant_id =   current_user.tenant_id
#     tenant_userslist = db.query(Tenant).filter(Tenant.id == tenant_id).first()
#     if not tenant_userslist:
#         raise HTTPException(status_code=400,
#                             detail = "unable to get tenant_userdetails")
        
#     return {
#         "Tenant_userdetails":tenant_userslist.users,
#         "message":"tenant user details"
#     }    


def tenant_userlist(
    current_user: User = Depends(get_current_user),
):
    tenant = current_user.tenant

    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    return {
        "tenant_id": tenant.id,
        "tenant_name": tenant.name,
        "users": tenant.users
    }
          