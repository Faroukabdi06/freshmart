from sqlalchemy import Column,Integer,String,DateTime,Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.cores.database import Base

from datetime import datetime,timezone
import uuid

class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable = True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default = lambda:datetime.now(timezone.utc))

    products = relationship("Product", back_populates = "category")

