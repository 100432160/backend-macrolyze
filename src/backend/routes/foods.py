from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from backend.core.database import get_db
from backend.schemas.food import FoodCreate, FoodResponse, FoodUpdate
from backend.services.food_service import (
    create_food, get_all_foods, get_food_by_id, update_food, delete_food
)

router = APIRouter(prefix="/api/foods", tags=["Foods"])

# Crear un nuevo alimento
@router.post("/", response_model=FoodResponse, status_code=201)
async def create_food_endpoint(food: FoodCreate, db: AsyncSession = Depends(get_db)):
    return await create_food(db, food)

# Obtener todos los alimentos
@router.get("/", response_model=list[FoodResponse])
async def get_all_foods_endpoint(user_id: UUID, db: AsyncSession = Depends(get_db)):
    return await get_all_foods(db, user_id)

# Obtener un alimento por ID
@router.get("/{food_id}", response_model=FoodResponse)
async def get_food_by_id_endpoint(food_id: UUID, db: AsyncSession = Depends(get_db)):
    food = await get_food_by_id(db, food_id)
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    return food

# Actualizar un alimento
@router.put("/{food_id}", response_model=FoodResponse)
async def update_food_endpoint(food_id: UUID, updates: FoodUpdate, db: AsyncSession = Depends(get_db)):
    updated_food = await update_food(db, food_id, updates)
    if not updated_food:
        raise HTTPException(status_code=404, detail="Food not found")
    return updated_food

# Eliminar un alimento
@router.delete("/{food_id}", status_code=204)
async def delete_food_endpoint(food_id: UUID, db: AsyncSession = Depends(get_db)):
    deleted_food = await delete_food(db, food_id)
    if not deleted_food:
        raise HTTPException(status_code=404, detail="Food not found")
