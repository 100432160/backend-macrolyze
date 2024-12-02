from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.database import get_db
from uuid import UUID
from backend.services.weekly_tracker_service import (
    get_weekly_summary,
    create_weekly_tracker,
)
from backend.schemas.weekly_tracker import WeeklySummaryResponse, WeeklyTrackerCreate, WeeklyTrackerResponse

router = APIRouter(prefix="/api/weekly_tracker", tags=["Weekly Tracker"])

@router.get("/{user_id}", response_model=WeeklySummaryResponse)
async def get_weekly_summary_route(user_id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        return await get_weekly_summary(user_id, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=WeeklyTrackerResponse)
async def create_weekly_tracker_route(
    tracker: WeeklyTrackerCreate, db: AsyncSession = Depends(get_db)
):
    try:
        weekly_tracker = await create_weekly_tracker(tracker, db)
        return weekly_tracker  # Devuelve directamente un esquema Pydantic
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
