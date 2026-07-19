from uuid import UUID
from datetime import date
from pydantic import BaseModel


class CustomerCreate(BaseModel):
    first_name: str
    middle_name: str | None = None
    last_name: str
    date_of_birth: date | None = None
    gender: str | None = None
    nationality: str | None = None
    mobile_number: str | None = None
    phone_number: str | None = None
    email: str | None = None
    secondary_email: str | None = None
    address: str | None = None
    permanent_address: str | None = None
    state: str | None = None
    district: str | None = None
    pin_code: str | None = None
    customer_status: str | None = None
    is_active: bool | None = True


class CustomerUpdate(CustomerCreate):
    pass


class CustomerResponse(CustomerCreate):
    id: UUID

    class Config:
        from_attributes = True