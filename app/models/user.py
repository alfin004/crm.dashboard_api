from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class User(Base):
    """Staff records owned by the auth/users table.

    This model deliberately does not inherit ``BaseModel`` because the users
    table does not contain the CRM ``is_deleted`` column.
    """

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True)
    username = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(255))
    mobile_number = Column(String(30))
    role = Column(String(30), nullable=False)
    is_active = Column(Boolean, nullable=False)
    current_login_status = Column(Boolean, nullable=False)
    last_login_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)
    created_by = Column(UUID(as_uuid=True))
    updated_by = Column(UUID(as_uuid=True))
