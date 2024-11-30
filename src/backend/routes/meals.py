from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from backend.core.database import get_db
from backend.schemas.meal import (
    MealCreate, MealResponse, MealUpdate, MealFoodCreate, MealFoodResponse
)
from backend.services.meal_service import (
    create_meal, get_meals_by_user_and_date, update_meal, delete_meal,
    add_food_to_meal, update_food_in_meal, remove_food_from_meal
)

router = APIRouter(prefix="/api/meals", tags=["Meals"])

# Crear una nueva comida
@router.post("/", response_model=MealResponse, status_code=201)
async def create_meal_endpoint(meal: MealCreate, db: AsyncSession = Depends(get_db)):
    return await create_meal(db, meal)

# Obtener comidas por usuario y fecha
@router.get("/{user_id}/{date}", response_model=list[MealResponse])
async def get_meals_by_user_and_date_endpoint(user_id: UUID, date: str, db: AsyncSession = Depends(get_db)):
    return await get_meals_by_user_and_date(db, user_id, date)

# Actualizar una comida
@router.put("/{meal_id}", response_model=MealResponse)
async def update_meal_endpoint(meal_id: UUID, updates: MealUpdate, db: AsyncSession = Depends(get_db)):
    return await update_meal(db, meal_id, updates)

# Eliminar una comida
@router.delete("/{meal_id}", status_code=204)
async def delete_meal_endpoint(meal_id: UUID, db: AsyncSession = Depends(get_db)):
    return await delete_meal(db, meal_id)

# Agregar un alimento a una comida
@router.post("/{meal_id}/foods", response_model=MealFoodResponse, status_code=201)
async def add_food_to_meal_endpoint(meal_id: UUID, food_data: MealFoodCreate, db: AsyncSession = Depends(get_db)):
    return await add_food_to_meal(db, meal_id, food_data)

# Actualizar la cantidad de un alimento en una comida
@router.put("/{meal_id}/foods/{food_id}", response_model=MealFoodResponse)
async def update_food_in_meal_endpoint(meal_id: UUID, food_id: UUID, quantity: float, db: AsyncSession = Depends(get_db)):
    return await update_food_in_meal(db, meal_id, food_id, quantity)

# Eliminar un alimento de una comida
@router.delete("/{meal_id}/foods/{food_id}", status_code=204)
async def remove_food_from_meal_endpoint(meal_id: UUID, food_id: UUID, db: AsyncSession = Depends(get_db)):
    return await remove_food_from_meal(db, meal_id, food_id)
