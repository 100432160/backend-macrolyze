from fastapi import APIRouter

router = APIRouter()

@router.get("/food_groups/")
async def get_food_groups():
    return {"message": "This is the food_groups endpoint"}
