from pydantic import BaseModel
from uuid import UUID
from datetime import date
from typing import List, Optional

# Esquema para representar cada día en el resumen semanal
class DailySummary(BaseModel):
    date: date
    total_proteins: float
    total_carbs: float
    total_fats: float
    total_kcals: float

# Esquema para la respuesta del resumen semanal
class WeeklySummaryResponse(BaseModel):
    week_start: date
    user_id: UUID
    summary: List[DailySummary]

# Esquema para crear un nuevo tracker semanal
class WeeklyTrackerCreate(BaseModel):
    user_id: UUID
    week_start: date

# Esquema para la respuesta al crear un tracker semanal
class WeeklyTrackerResponse(BaseModel):
    id: UUID
    user_id: UUID
    week_start: date

    class Config:
        from_attributes = True  # Habilita conversión desde modelos SQLAlchemy
