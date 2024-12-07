from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.core.database import Base
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    meals = relationship("Meal", back_populates="user")
    foods = relationship("Food", back_populates="user")
    food_groups = relationship("FoodGroup", back_populates="user", cascade="all, delete-orphan")
    weekly_trackers = relationship("WeeklyTracker", back_populates="user")
