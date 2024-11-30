from pydantic import BaseModel
from uuid import UUID
from datetime import date
from typing import Optional

# Esquema base para una comida
class MealBase(BaseModel):
    type: str  # Tipo de comida (e.g., desayuno, almuerzo, cena)
    date: date

# Esquema para crear una nueva comida
class MealCreate(MealBase):
    user_id: UUID

# Esquema para actualizar una comida existente
class MealUpdate(BaseModel):
    type: Optional[str] = None
    date: Optional[date] = None

# Esquema para la respuesta de una comida
class MealResponse(MealBase):
    id: UUID
    user_id: UUID

    class Config:
        from_attributes = True

# Esquema para crear una relación Meal-Food
class MealFoodCreate(BaseModel):
    meal_id: UUID
    food_id: UUID
    quantity: float

class MealFoodResponse(BaseModel):
    meal_id: UUID
    food_id: UUID
    quantity: float  # Cantidad de alimento

    class Config:
        from_attributes = True
