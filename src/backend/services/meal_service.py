from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from backend.models.meal import Meal
from backend.models.meal_food import MealFood
from backend.schemas.meal import MealCreate, MealUpdate, MealFoodCreate
from fastapi import HTTPException

# Crear una nueva comida
async def create_meal(db: AsyncSession, meal_data: MealCreate):
    new_meal = Meal(user_id=meal_data.user_id, type=meal_data.type, date=meal_data.date)
    db.add(new_meal)
    await db.commit()
    await db.refresh(new_meal)
    return new_meal

# Obtener todas las comidas de un usuario
async def get_all_meals_by_user_service(db: AsyncSession, user_id: UUID):
    result = await db.execute(select(Meal).where(Meal.user_id == user_id))
    return result.scalars().all()

# Obtener comidas de un usuario en una fecha específica
async def get_meals_by_user_and_date(db: AsyncSession, user_id: UUID, date: str):
    result = await db.execute(select(Meal).where(Meal.user_id == user_id, Meal.date == date))
    return result.scalars().all()

# Actualizar una comida
async def update_meal(db: AsyncSession, meal_id: UUID, updates: MealUpdate):
    result = await db.execute(select(Meal).where(Meal.id == meal_id))
    meal = result.scalars().first()
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")

    if updates.type:
        meal.type = updates.type
    if updates.date:
        meal.date = updates.date

    await db.commit()
    await db.refresh(meal)
    return meal

# Eliminar una comida
async def delete_meal(db: AsyncSession, meal_id: UUID):
    result = await db.execute(select(Meal).where(Meal.id == meal_id))
    meal = result.scalars().first()
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")

    await db.delete(meal)
    await db.commit()
    return None

# Agregar un alimento a una comida
async def add_food_to_meal(db: AsyncSession, meal_id: UUID, food_data: MealFoodCreate):
    new_meal_food = MealFood(meal_id=meal_id, food_id=food_data.food_id, quantity=food_data.quantity)
    db.add(new_meal_food)
    await db.commit()
    await db.refresh(new_meal_food)
    return new_meal_food

# Actualizar la cantidad de un alimento en una comida
async def update_food_in_meal(db: AsyncSession, meal_id: UUID, food_id: UUID, quantity: float):
    result = await db.execute(select(MealFood).where(MealFood.meal_id == meal_id, MealFood.food_id == food_id))
    meal_food = result.scalars().first()
    if not meal_food:
        raise HTTPException(status_code=404, detail="Food not found in meal")

    meal_food.quantity = quantity
    await db.commit()
    await db.refresh(meal_food)
    return meal_food

# Eliminar un alimento de una comida
async def remove_food_from_meal(db: AsyncSession, meal_id: UUID, food_id: UUID):
    result = await db.execute(select(MealFood).where(MealFood.meal_id == meal_id, MealFood.food_id == food_id))
    meal_food = result.scalars().first()
    if not meal_food:
        raise HTTPException(status_code=404, detail="Food not found in meal")

    await db.delete(meal_food)
    await db.commit()
    return None
