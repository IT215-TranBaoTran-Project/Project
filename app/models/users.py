from datetime import datetime, timezone

from sqlalchemy import Column,Integer,String,Boolean,DateTime
from sqlalchemy.orm import relationship

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,autoincrement=True)
    email = Column(String(255),unique=True,nullable=False)
    full_name = Column(String(255),nullable=False)
    password_hash = Column(String(255),nullable=False)
    role = Column(String(20),default="USER",nullable=False)
    is_active = Column(Boolean,default=True,nullable=False)
    created_at = Column(DateTime,default=datetime.now(timezone.utc))
    updated_at = Column(DateTime,default=datetime.now(timezone.utc),onupdate=datetime.now(timezone.utc))

    owned_campaigns = relationship("Campaign",back_populates="owner")
    campaign_memberships = relationship("CampaignMember",back_populates="user")