import uuid
from sqlalchemy import Column, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.core.database import Base

class FoodGroupItem(Base):
    __tablename__ = "food_group_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    food_group_id = Column(UUID(as_uuid=True), ForeignKey("food_groups.id"), nullable=False)
    food_id = Column(UUID(as_uuid=True), ForeignKey("foods.id"), nullable=False)
    default_quantity = Column(Float, nullable=False)

    food_group = relationship("FoodGroup", back_populates="items")
    food = relationship("Food", back_populates="food_group_items", lazy="joined")
