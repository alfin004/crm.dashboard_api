from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel


class CustomerProduct(BaseModel):
    __tablename__ = "customer_products"

    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    assigned_staff_id = Column(UUID(as_uuid=True))
