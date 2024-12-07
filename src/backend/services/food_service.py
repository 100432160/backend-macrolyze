from uuid import UUID

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.food import Food
from backend.schemas.food import FoodCreate, FoodUpdate

# Crear un nuevo alimento
async def create_food(db: AsyncSession, food: FoodCreate):
    new_food = Food(
        food_name=food.food_name,
        proteins=food.proteins,
        carbs=food.carbs,
        fats=food.fats,
        kcals=food.kcals,
        user_id=food.user_id
    )
    db.add(new_food)
    await db.commit()
    await db.refresh(new_food)
    return new_food

# Obtener todos los alimentos
async def get_all_foods(db: AsyncSession, user_id: UUID):
    result = await db.execute(select(Food).where(Food.user_id == user_id))
    return result.scalars().all()

# Obtener un alimento por ID
async def get_food_by_id(db: AsyncSession, food_id: UUID):
    result = await db.execute(select(Food).where(Food.id == food_id))
    return result.scalars().first()

# Actualizar un alimento
async def update_food(db: AsyncSession, food_id: UUID, updates: FoodUpdate):
    food = await get_food_by_id(db, food_id)
    if not food:
        return None

    for key, value in updates.dict(exclude_unset=True).items():
        setattr(food, key, value)

    await db.commit()
    await db.refresh(food)
    return food

# Eliminar un alimento
async def delete_food(db: AsyncSession, food_id: UUID):
    food = await get_food_by_id(db, food_id)
    if not food:
        return None

    await db.delete(food)
    await db.commit()
    return food
