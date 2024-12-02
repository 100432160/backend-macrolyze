from backend.models.user import User
from backend.models.food import Food
from backend.models.meal import Meal
from backend.models.meal_food import MealFood
from backend.models.food_group import FoodGroup
from backend.models.food_group_item import FoodGroupItem

# Importa el Base compartido
from backend.core.database import Base

# Asegúrate de registrar todos los modelos en `__all__` para evitar problemas
__all__ = ["User", "Food", "Meal", "MealFood", "FoodGroup", "FoodGroupItem", "Base"]
