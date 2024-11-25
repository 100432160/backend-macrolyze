from fastapi import APIRouter

router = APIRouter()

@router.get("/weekly_tracker/")
async def get_weekly_tracker():
    return {"message": "This is the weekly_tracker endpoint"}
