from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from backend.core.database import Base
import uuid
from sqlalchemy.orm import relationship

class Food(Base):
    __tablename__ = "foods"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    food_name = Column(String, nullable=False, unique=True)
    proteins = Column(Float, nullable=False)
    carbs = Column(Float, nullable=False)
    fats = Column(Float, nullable=False)
    kcals = Column(Float, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)  # Nuevo campo

    # Relación hacia el modelo User
    user = relationship("User", back_populates="foods")  # Relación bidireccional

    meal_foods = relationship("MealFood", back_populates="food")
    food_group_items = relationship("FoodGroupItem", back_populates="food")
