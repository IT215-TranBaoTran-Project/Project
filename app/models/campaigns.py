from datetime import datetime, timezone

from sqlalchemy import Column,Integer,String,Text,DateTime,ForeignKey,Enum
from sqlalchemy.orm import relationship

from app.db.database import Base


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(255),nullable=False)
    description = Column(Text,nullable=True)
    owner_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    created_at = Column(DateTime,default=datetime.now(timezone.utc))
    updated_at = Column(DateTime,default=datetime.now(timezone.utc),onupdate=datetime.now(timezone.utc))

    owner = relationship("User",back_populates="owned_campaigns")
    members = relationship(
        "CampaignMember",
        back_populates="campaign",
        cascade="all, delete-orphan"
    )
    tasks = relationship(
        "CampaignTask",
        back_populates="campaign",
        cascade="all, delete-orphan"
    )


class CampaignMember(Base):
    __tablename__ = "campaign_members"

    id = Column(Integer,primary_key=True,autoincrement=True)
    campaign_id = Column(Integer,ForeignKey("campaigns.id"),nullable=False)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    role = Column(Enum("OWNER","MEMBER"),nullable=False)
    joined_at = Column(DateTime,default=datetime.now(timezone.utc))

    campaign = relationship("Campaign",back_populates="members")
    user = relationship("User",back_populates="campaign_memberships")


class CampaignTask(Base):
    __tablename__ = "campaign_tasks"

    id = Column(Integer,primary_key=True,autoincrement=True)
    campaign_id = Column(Integer,ForeignKey("campaigns.id"),nullable=False)
    title = Column(String(255),nullable=False)
    description = Column(Text,nullable=True)
    due_date = Column(DateTime,nullable=True)
    priority = Column(String(50),nullable=True)
    created_at = Column(DateTime,default=datetime.now(timezone.utc))
    updated_at = Column(DateTime,default=datetime.now(timezone.utc),onupdate=datetime.now(timezone.utc))

    campaign = relationship("Campaign",back_populates="tasks")