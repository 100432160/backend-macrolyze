from sqlalchemy import Column, String, Float
from sqlalchemy.dialects.postgresql import UUID
from backend.core.base import Base
import uuid

class Food(Base):
    __tablename__ = "foods"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    food_name = Column(String, nullable=False, unique=True)
    proteins = Column(Float, nullable=False)
    carbs = Column(Float, nullable=False)
    fats = Column(Float, nullable=False)
    kcals = Column(Float, nullable=False)
