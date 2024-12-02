from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.models.food_group import FoodGroup
from backend.models.food_group_item import FoodGroupItem
from backend.schemas.food_group import FoodGroupCreate, FoodGroupUpdate, FoodGroupItemCreate
from uuid import UUID
from fastapi import HTTPException

# Create a new food group
async def create_food_group(db: AsyncSession, food_group_data: FoodGroupCreate):
    new_group = FoodGroup(**food_group_data.dict())
    db.add(new_group)
    await db.commit()
    await db.refresh(new_group)
    return new_group

# Get all food groups for a user
async def get_food_groups_by_user(db: AsyncSession, user_id: UUID):
    result = await db.execute(select(FoodGroup).where(FoodGroup.user_id == user_id))
    return result.scalars().all()

# Update a food group
async def update_food_group(db: AsyncSession, group_id: UUID, updates: FoodGroupUpdate):
    group = await db.get(FoodGroup, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Food group not found")

    for key, value in updates.dict(exclude_unset=True).items():
        setattr(group, key, value)

    await db.commit()
    await db.refresh(group)
    return group

# Delete a food group
async def delete_food_group(db: AsyncSession, group_id: UUID):
    group = await db.get(FoodGroup, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Food group not found")

    await db.delete(group)
    await db.commit()
    return True

# Add a food to a food group
async def add_food_to_group(db: AsyncSession, food_item_data: FoodGroupItemCreate):
    new_item = FoodGroupItem(**food_item_data.dict())
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item

# Update default quantity of a food in a group
async def update_food_in_group(db: AsyncSession, group_id: UUID, food_id: UUID, quantity: float):
    item = await db.execute(select(FoodGroupItem).where(
        FoodGroupItem.food_group_id == group_id,
        FoodGroupItem.food_id == food_id
    ))
    item = item.scalars().first()
    if not item:
        raise HTTPException(status_code=404, detail="Food item not found in group")

    item.default_quantity = quantity
    await db.commit()
    await db.refresh(item)
    return item

# Remove a food from a food group
async def remove_food_from_group(db: AsyncSession, group_id: UUID, food_id: UUID):
    item = await db.execute(select(FoodGroupItem).where(
        FoodGroupItem.food_group_id == group_id,
        FoodGroupItem.food_id == food_id
    ))
    item = item.scalars().first()
    if not item:
        raise HTTPException(status_code=404, detail="Food item not found in group")

    await db.delete(item)
    await db.commit()
    return True
