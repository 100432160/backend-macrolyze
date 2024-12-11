from pydantic import BaseModel
from uuid import UUID
from datetime import date
from typing import Optional, List
from backend.schemas.food import FoodResponse, FoodInMealResponse, FoodMealResponse

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

class MealFoodCreateResponse(BaseModel):
    meal_id: UUID
    food_id: FoodMealResponse
    quantity: float  # Cantidad de alimento

    class Config:
        from_attributes = True

# Esquema para la respuesta de obtener todos los alimentos de una comida
class MealWithFoodsResponse(BaseModel):
    meal_id: UUID
    type: str
    date: date
    foods: List[FoodInMealResponse]  # Lista de alimentos asociados a la comida

    class Config:
        from_attributes = True
