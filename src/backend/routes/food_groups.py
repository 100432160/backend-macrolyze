from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from backend.core.database import get_db
from backend.schemas.food_group import (
    FoodGroupCreate, FoodGroupResponse, FoodGroupUpdate, FoodGroupItemCreate, FoodGroupItemResponse
)
from backend.services.food_group_service import (
    create_food_group, get_food_groups_by_user, update_food_group, delete_food_group,
    add_food_to_group, update_food_in_group, remove_food_from_group
)

router = APIRouter(prefix="/api/food_groups", tags=["Food Groups"])

@router.post("/", response_model=FoodGroupResponse)
async def create_group(data: FoodGroupCreate, db: AsyncSession = Depends(get_db)):
    return await create_food_group(db, data)

@router.get("/{user_id}", response_model=list[FoodGroupResponse])
async def get_groups(user_id: UUID, db: AsyncSession = Depends(get_db)):
    return await get_food_groups_by_user(db, user_id)

@router.put("/{group_id}", response_model=FoodGroupResponse)
async def update_group(group_id: UUID, data: FoodGroupUpdate, db: AsyncSession = Depends(get_db)):
    return await update_food_group(db, group_id, data)

@router.delete("/{group_id}")
async def delete_group(group_id: UUID, db: AsyncSession = Depends(get_db)):
    await delete_food_group(db, group_id)
    return {"success": True}

@router.post("/{group_id}/foods", response_model=FoodGroupItemResponse)
async def add_food(group_id: UUID, data: FoodGroupItemCreate, db: AsyncSession = Depends(get_db)):
    return await add_food_to_group(db, data)

@router.put("/{group_id}/foods/{food_id}", response_model=FoodGroupItemResponse)
async def update_food(group_id: UUID, food_id: UUID, quantity: float, db: AsyncSession = Depends(get_db)):
    return await update_food_in_group(db, group_id, food_id, quantity)

@router.delete("/{group_id}/foods/{food_id}")
async def remove_food(group_id: UUID, food_id: UUID, db: AsyncSession = Depends(get_db)):
    await remove_food_from_group(db, group_id, food_id)
    return {"success": True}
