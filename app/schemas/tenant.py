from pydantic import BaseModel

class TenantCreate(BaseModel):
    name:str
    subdomain:str
    is_active:bool
    
class Config:
        from_attributes = True        