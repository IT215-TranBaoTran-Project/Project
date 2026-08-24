from sqlalchemy import Column,Integer,String,Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime, timezone

class Users(Base):
    __tablename__ ='users'
    
    id = Column(Integer,primary_key=True,index=True)
    email = Column(String(255),unique=True,nullable=False)
    password_hash = Column(String(255),nullable=False)
    full_name = Column(String(255),nullable=False)
    role = Column(String(20),Enum('USER','ADMIN'),default="USER",nullable=False)
    is_active = Column(Boolean,default=True,nullable=False)
    created_at = Column(DateTime,default=datetime.now(timezone.utc))
    
    campaigns = relationship("Campaign",back_populates="owner")
    campaign_member = relationship('CampaignMember', back_populates='user')
    campaign_task = relationship('CampaignTasks', back_populates='users')