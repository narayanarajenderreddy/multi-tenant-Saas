from pydantic import BaseModel,EmailStr

class UserCreate(BaseModel):
    username:str
    email:EmailStr
    password:str
    tenant_id:int
    mobile_number :str
    
    
class UserLogin(BaseModel):
    email:EmailStr
    password:str


class UserResponse(BaseModel):
    id:int
    username:str
    email:EmailStr
    tenant_id:int
    
    
    class Config:
        from_attributes = True      