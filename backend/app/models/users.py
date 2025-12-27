from sqlalchemy import Column,Integer,String,DateTime,ForeignKey,Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.cores.database import Base

from datetime import datetime,timezone
import enum
import uuid

class UserRole(str,enum.Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"

class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key = True,
        default = uuid.uuid4,
        index=True

    )
    name = Column(String,nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable = False)
    role = Column(
        SQLEnum(UserRole, name="user_role"),
        nullable = False,
        default = UserRole.CUSTOMER
    )
    created_at = Column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc))