from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class CampaignTask(Base):
    __tablename__ = "campaign_tasks"

    id = Column(Integer, primary_key=True, index=True)

    campaign_id = Column(
        Integer,
        ForeignKey("campaigns.id"),
        nullable=False
    )

    assignee_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    title = Column(
        String(255),
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    due_date = Column(
        DateTime,
        nullable=True
    )

    status = Column(
        String(50),
        nullable=False,
        default="TODO"
    )

    priority = Column(
        String(50),
        nullable=True,
        default="MEDIUM"
    )

    created_at = Column(
        DateTime,
        default=datetime.now(timezone.utc)
    )

    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc)
    )

    campaign = relationship(
        "Campaign",
        back_populates="tasks"
    )

    assignee = relationship(
        "User",
        foreign_keys=[assignee_id]
    )