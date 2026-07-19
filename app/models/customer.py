from sqlalchemy import Column, String, Date, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel


class Customer(BaseModel):
    __tablename__ = "customers"

    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(Date)
    gender = Column(String)
    nationality = Column(String)
    mobile_number = Column(String)
    phone_number = Column(String)
    email = Column(String)
    secondary_email = Column(String)
    address = Column(String)
    permanent_address = Column(String)
    state = Column(String)
    district = Column(String)
    pin_code = Column(String)
    assigned_staff_id = Column(UUID(as_uuid=True))
    customer_status = Column(String)
    is_active = Column(Boolean, default=True)
    created_by = Column(UUID(as_uuid=True))