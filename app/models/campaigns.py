from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db.database import Base

from datetime import datetime, timezone


class Campaign(Base):
    __tablename__ ='campaigns'
    
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(255),nullable=False)
    description = Column(Text,nullable=True)
    owner_id = Column(Integer,ForeignKey('users.id'),nullable=False)

    created_at = Column(DateTime,nullable=False)

    created_at = Column(DateTime,default=datetime.now(timezone.utc))
    
    owner = relationship('Users', back_populates='campaigns')
    campaigns_member = relationship('CampaignMember', back_populates='campaign')
    campaigns_task = relationship('CampaignTasks', back_populates='campaign')
    
    
class CampaignMember(Base):
    __tablename__ = 'campaign_members'
    
    campaign_id = Column(Integer,ForeignKey('campaigns.id'), primary_key=True)
    users_id = Column(Integer,ForeignKey('users.id'), primary_key=True)
    role = Column(Enum('OWNER','MEMBER'),default='OWNER')

    joined_at = Column(DateTime,nullable=False)

    joined_at = Column(DateTime,default=datetime.now(timezone.utc))
    
    user = relationship('Users', back_populates='campaign_member')
    campaign = relationship('Campaign', back_populates='campaigns_member')
