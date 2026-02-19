from sqlalchemy import Column,Integer,Boolean,String,ForeignKey,DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,nullable=False)
    description = Column(String,nullable=False)
    tenant_id = Column(Integer,ForeignKey("tenants.id"),nullable=False)
    created_by = Column(Integer,ForeignKey("users.id"),nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    tenant = relationship("Tenant")
    creator = relationship("User")