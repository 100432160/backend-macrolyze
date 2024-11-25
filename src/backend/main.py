from fastapi import FastAPI
from backend.routes import users, foods, meals, food_groups, weekly_tracker

app = FastAPI(title="Macrolyze API")

# Incluir los routers
app.include_router(users.router)
app.include_router(foods.router)
app.include_router(meals.router)
app.include_router(food_groups.router)
app.include_router(weekly_tracker.router)

@app.get("/")
def root():
    return {"message": "Welcome to Macrolyze API"}
