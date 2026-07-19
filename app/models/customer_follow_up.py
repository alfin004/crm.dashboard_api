import enum

from sqlalchemy import Column, String, Date, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel


class FollowUpStatus(str, enum.Enum):
    PENDING = "pending"
    CONTACTED = "contacted"
    INTERESTED = "interested"
    NOT_INTERESTED = "not_interested"
    FOLLOW_UP_SCHEDULED = "follow_up_scheduled"
    CONVERTED = "converted"
    LOST = "lost"


class CustomerFollowUp(BaseModel):
    __tablename__ = "customer_follow_ups"

    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    status = Column(Enum(FollowUpStatus, name="follow_up_status"), nullable=False)
    target_date = Column(Date)
    current_date = Column(Date)
    description = Column(String, nullable=False)
    followed_up_by = Column(UUID(as_uuid=True))
