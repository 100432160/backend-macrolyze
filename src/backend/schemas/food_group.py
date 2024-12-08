from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional

# Base schema for FoodGroup
class FoodGroupBase(BaseModel):
    group_name: str

class FoodGroupCreate(FoodGroupBase):
    user_id: UUID

class FoodGroupUpdate(BaseModel):
    group_name: Optional[str] = None

class FoodGroupResponse(FoodGroupBase):
    id: UUID
    user_id: UUID

    class Config:
        from_attributes = True

# Schema for FoodGroupItem
class FoodGroupItemBase(BaseModel):
    default_quantity: float

class FoodGroupItemCreate(FoodGroupItemBase):
    food_group_id: UUID
    food_id: UUID

class FoodGroupItemResponse(FoodGroupItemBase):
    id: UUID
    food_group_id: UUID
    food_id: UUID
    food_name: str  # Añadimos el nombre del alimento
    default_quantity: float  # Añadimos la cantidad predeterminada
    protein_per_100g: float  # Proteínas por cada 100 g
    carbs_per_100g: float  # Carbohidratos por cada 100 g
    fats_per_100g: float  # Grasas por cada 100 g
    calories_per_100g: float  # Calorías por cada 100 g

    class Config:
        from_attributes = True
