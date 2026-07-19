from sqlalchemy import Column, String
from app.models.base import BaseModel

class Product(BaseModel):
    __tablename__ = "products"
    product_code = Column(String, unique=True, nullable=False)
    product_name = Column(String, nullable=False)
    product_description = Column(String)
    status = Column(String)
    created_by = Column(String)
