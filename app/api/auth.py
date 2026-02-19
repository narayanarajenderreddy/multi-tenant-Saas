from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.core.security import hash_password, verify_password, create_access_token
from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/me",response_model = UserResponse)
def get_me(current_user:User = Depends(get_current_user)):
    return current_user


@router.post('/register',response_model=UserResponse)
def user_register(user_data:UserCreate,db:Session = Depends(get_db)):
    existing_user  = db.query(User).filter(User.email == user_data.email).first()
    
    if existing_user:
        raise HTTPException(
            status_code=400,
            message = "Already email has been registered"
        )
    
    new_user_register = User(
        email = user_data.email,
        username = user_data.username,
        hashed_password = hash_password(user_data.password),
        tenant_id = user_data.tenant_id,
        mobile_number = user_data.mobile_number
    )
    
    db.add(new_user_register)
    db.commit()
    db.refresh(new_user_register)   
    
    return new_user_register 


@router.post("/login")
def userlogin(user_data:UserLogin,db:Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    
    if not user:
        raise HTTPException(
            status_code=400,
            message = "Invalid Credentials"
        )
    if not  user.is_active:
        raise HTTPException(status_code=400,message = "User is inactive")
    
    
    if not verify_password(user_data.password,user.hashed_password):
        raise HTTPException(status_code=400,message = "Invalid credentials")
    
    
    create_token = create_access_token({
        "user_id":user.id,
        "tenant_id":user.tenant_id,
        "is_super_admin":user.is_super_admin
    })
    
    return {
        "access_token":create_token,
        "token_type":"bearer"
    }
    
