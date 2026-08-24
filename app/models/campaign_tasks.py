from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db.database import Base

from datetime import datetime,timezone

class CampaignTasks(Base):
    __tablename__ = 'campaign_tasks'
    
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    assignee_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    status = Column(Enum('TODO', 'IN_PROGRESS', 'DONE'), nullable=False, default='TODO')
    pririty = Column(Enum('LOW', 'MEDIUM', 'HIGH'), nullable=False, default='MEDIUM')
    due_date = Column(DateTime, nullable=False)

    created_at = Column(DateTime, nullable=False)

    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    
    users = relationship('Users', back_populates='campaign_task')
    campaign = relationship('Campaign', back_populates='campaigns_task')