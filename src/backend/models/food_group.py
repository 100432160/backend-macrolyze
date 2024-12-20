from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.core.database import Base
import uuid

class FoodGroup(Base):
    __tablename__ = "food_groups"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    group_name = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="food_groups")
    items = relationship("FoodGroupItem", back_populates="food_group", cascade="all, delete-orphan")
