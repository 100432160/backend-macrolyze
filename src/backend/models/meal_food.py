from sqlalchemy import Column, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.core.database import Base

class MealFood(Base):
    __tablename__ = "meal_foods"

    meal_id = Column(UUID(as_uuid=True), ForeignKey("meals.id"), primary_key=True)
    food_id = Column(UUID(as_uuid=True), ForeignKey("foods.id"), primary_key=True)
    quantity = Column(Float, nullable=False)

    meal = relationship("Meal", back_populates="meal_foods")
    food = relationship("Food")
