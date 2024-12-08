from fastapi import FastAPI
from backend.routes import users, foods, meals, food_groups, weekly_tracker
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Macrolyze API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Especifica el dominio del frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

# Incluir los routers
app.include_router(users.router)
app.include_router(foods.router)
app.include_router(meals.router)
app.include_router(food_groups.router)
app.include_router(weekly_tracker.router)

@app.middleware("http")
async def log_requests(request, call_next):
    print(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    print(f"Response status: {response.status_code}")
    return response

@app.get("/")
def root():
    return {"message": "Welcome to Macrolyze API"}
