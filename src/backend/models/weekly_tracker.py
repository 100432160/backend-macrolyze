import uuid
from sqlalchemy import Column, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.core.database import Base

class WeeklyTracker(Base):
    __tablename__ = "weekly_trackers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    week_start = Column(Date, nullable=False)  # Fecha de inicio de la semana
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="weekly_trackers")  # Relación con User
    # No es necesario agregar relación con meals directamente
