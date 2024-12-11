from pydantic import BaseModel
from uuid import UUID

# Esquema base
class FoodBase(BaseModel):
    food_name: str
    proteins: float
    carbs: float
    fats: float
    kcals: float

# Esquema para crear alimentos
class FoodCreate(FoodBase):
    user_id: UUID

# Esquema para actualizar alimentos
class FoodUpdate(BaseModel):
    proteins: float = None
    carbs: float = None
    fats: float = None
    kcals: float = None

# Esquema para la respuesta
class FoodInMealResponse(FoodBase):
    id: UUID
    user_id: UUID
    food_name: str
    proteins: float
    carbs: float
    fats: float
    kcals: float
    quantity: float

    class Config:
        from_attributes = True

# Esquema para la respuesta
class FoodMealResponse(FoodBase):
    id: UUID
    user_id: UUID
    food_name: str
    proteins: float
    carbs: float
    fats: float
    kcals: float

    class Config:
        from_attributes = True

# Esquema para la respuesta
class FoodResponse(FoodBase):
    id: UUID
    user_id: UUID
    proteins: float
    carbs: float
    fats: float
    kcals: float

    class Config:
        from_attributes = True
