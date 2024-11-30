from backend.models.user import User
from backend.models.food import Food
from backend.models.meal import Meal
from backend.models.meal_food import MealFood

from backend.core.database import Base  # Base compartida

# Registra explícitamente los modelos en Base.metadata
__all__ = ["User", "Food", "Meal", "MealFood"]
