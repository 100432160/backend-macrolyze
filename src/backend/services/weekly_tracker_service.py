from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from backend.models import WeeklyTracker, Meal
from backend.schemas.weekly_tracker import WeeklySummaryResponse, DailySummary, WeeklyTrackerCreate, WeeklyTrackerResponse

async def get_weekly_summary(user_id: UUID, session: AsyncSession):
    # Obtener las comidas del usuario para la semana
    meals = await session.execute(
        select(Meal).where(Meal.user_id == user_id)
    )
    meals = meals.scalars().all()

    # Crear un diccionario para almacenar el resumen diario
    daily_summary = {}

    for meal in meals:
        day = meal.date.isoformat()  # Agrupar por día
        if day not in daily_summary:
            daily_summary[day] = {
                "total_proteins": 0,
                "total_carbs": 0,
                "total_fats": 0,
                "total_kcals": 0,
            }

        # Procesar alimentos dentro de la comida si existen
        if hasattr(meal, "foods") and meal.foods:
            for food in meal.foods:
                daily_summary[day]["total_proteins"] += food.proteins
                daily_summary[day]["total_carbs"] += food.carbs
                daily_summary[day]["total_fats"] += food.fats
                daily_summary[day]["total_kcals"] += food.kcals

    # Retornar el resumen semanal
    return {
        "week_start": min(daily_summary.keys()),
        "user_id": user_id,
        "summary": [
            {"date": day, **macros} for day, macros in daily_summary.items()
        ],
    }

async def create_weekly_tracker(data: WeeklyTrackerCreate, session: AsyncSession):
    weekly_tracker = WeeklyTracker(**data.dict())
    session.add(weekly_tracker)
    await session.commit()
    await session.refresh(weekly_tracker)
    return WeeklyTrackerResponse.from_orm(weekly_tracker)
