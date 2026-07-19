from uuid import UUID
from datetime import date
from pydantic import BaseModel

from app.models.customer_follow_up import FollowUpStatus


class FollowUpCreate(BaseModel):
    status: FollowUpStatus
    target_date: date | None = None
    current_date: date | None = None
    description: str


class FollowUpResponse(FollowUpCreate):
    id: UUID
    customer_id: UUID
    followed_up_by: UUID | None = None

    class Config:
        from_attributes = True
