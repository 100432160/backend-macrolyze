from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
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
    # Crear un nuevo FoodGroupItem
    new_item = FoodGroupItem(**food_item_data.dict())
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)

    # Cargar la relación con Food y asegurar que el food_name esté disponible
    item_with_food = await db.execute(
        select(FoodGroupItem)
        .options(joinedload(FoodGroupItem.food))  # Carga la relación con Food
        .where(FoodGroupItem.id == new_item.id)
    )
    item_with_food = item_with_food.scalars().first()

    if not item_with_food:
        raise HTTPException(status_code=404, detail="Food item not found in group")

    # Construir y devolver la respuesta
    return {
        "id": item_with_food.id,
        "food_group_id": item_with_food.food_group_id,
        "food_id": item_with_food.food_id,
        "food_name": item_with_food.food.food_name,  # Accede al nombre del alimento
        "default_quantity": item_with_food.default_quantity,
        "protein_per_100g": item_with_food.food.proteins,  # Obtener desde Food
        "carbs_per_100g": item_with_food.food.carbs,
        "fats_per_100g": item_with_food.food.fats,
        "calories_per_100g": item_with_food.food.kcals,
    }

# Get all foods in a food group
async def get_foods_by_group(db: AsyncSession, group_id: UUID):
    result = await db.execute(
        select(FoodGroupItem)
        .options(joinedload(FoodGroupItem.food))  # Carga la relación con la tabla Food
        .where(FoodGroupItem.food_group_id == group_id)
    )
    items = result.scalars().all()

    # Transformar los resultados para incluir food_name
    response = [
        {
            "id": item.id,
            "food_group_id": item.food_group_id,
            "food_id": item.food_id,
            "food_name": item.food.food_name,  # Acceso al nombre del alimento
            "default_quantity": item.default_quantity,
            "protein_per_100g": item.food.proteins,
            "carbs_per_100g": item.food.carbs,
            "fats_per_100g": item.food.fats,
            "calories_per_100g": item.food.kcals,
        }
        for item in items
    ]

    return response

# Update default quantity of a food in a group
# Update default quantity of a food in a group
async def update_food_in_group(db: AsyncSession, group_id: UUID, group_item_id: UUID, quantity: float):
    # Obtener el alimento dentro del grupo con la relación a Food
    item = await db.execute(
        select(FoodGroupItem)
        .options(joinedload(FoodGroupItem.food))  # Asegura que se cargue la relación con Food
        .where(
            FoodGroupItem.food_group_id == group_id,
            FoodGroupItem.id == group_item_id
        )
    )
    item = item.scalars().first()

    if not item:
        raise HTTPException(status_code=404, detail="Food item not found in group")

    # Actualizar la cantidad predeterminada
    item.default_quantity = quantity
    await db.commit()
    await db.refresh(item)

    # Construir y retornar una respuesta completa
    return {
        "id": item.id,
        "food_group_id": item.food_group_id,
        "food_id": item.food_id,
        "food_name": item.food.food_name,  # Acceso al nombre del alimento
        "default_quantity": item.default_quantity,
        "protein_per_100g": item.food.proteins,  # Incluye los macronutrientes
        "carbs_per_100g": item.food.carbs,
        "fats_per_100g": item.food.fats,
        "calories_per_100g": item.food.kcals,
    }

# Remove a food from a food group by group_item_id
async def remove_food_group_item_by_id(db: AsyncSession, group_id: UUID, group_item_id: UUID):
    # Busca el item en la base de datos usando `group_item_id` y `group_id`
    item = await db.execute(
        select(FoodGroupItem).where(
            FoodGroupItem.id == group_item_id,
            FoodGroupItem.food_group_id == group_id
        )
    )
    item = item.scalars().first()
    
    # Verifica si el item existe
    if not item:
        raise HTTPException(status_code=404, detail="Food item not found in the specified group")

    # Elimina el item si existe
    await db.delete(item)
    await db.commit()
    return True

