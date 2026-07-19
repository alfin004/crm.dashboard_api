from uuid import UUID
from pydantic import BaseModel


class AssignmentResponse(BaseModel):
    id: UUID
    customer_id: UUID
    product_id: UUID
    assigned_staff_id: UUID | None = None

    class Config:
        from_attributes = True
