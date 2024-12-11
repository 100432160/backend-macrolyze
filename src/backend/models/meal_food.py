from sqlalchemy import Column, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.core.database import Base
import uuid

class MealFood(Base):
    __tablename__ = "meal_foods"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    meal_id = Column(UUID(as_uuid=True), ForeignKey("meals.id"))
    food_id = Column(UUID(as_uuid=True), ForeignKey("foods.id"))
    quantity = Column(Float, nullable=False)

    meal = relationship("Meal", back_populates="meal_foods")
    food = relationship("Food", back_populates="meal_foods")
