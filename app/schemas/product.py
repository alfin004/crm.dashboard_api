from uuid import UUID
from pydantic import BaseModel

class ProductCreate(BaseModel):
    product_code:str
    product_name:str
    product_description:str|None=None
    status:str|None=None

class ProductUpdate(ProductCreate):
    pass

class ProductResponse(ProductCreate):
    id:UUID
    class Config:
        from_attributes=True
