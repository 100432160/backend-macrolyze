from sqlalchemy.future import select
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from typing import List
from uuid import UUID
from passlib.context import CryptContext
from backend.core.database import get_db
from backend.models.user import User
from backend.schemas.user import UserCreate, UserResponse, UserUpdate, UserLogin
from backend.services.user_service import update_user_service


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/api/users", tags=["Users"])

# Crear un nuevo usuario
@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Verificar si el usuario ya existe
    stmt = select(User).where(User.email == user.email)
    result = await db.execute(stmt)
    db_user = result.scalars().first()

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hashear la contraseña
    hashed_password = pwd_context.hash(user.password)

    # Crear el nuevo usuario
    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

# Obtener todos los usuarios
@router.get("/", response_model=list[UserResponse])
async def get_users_endpoint(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

# Obtener un usuario por ID
@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Actualizar un usuario
@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: UUID, updates: UserUpdate, db: AsyncSession = Depends(get_db)):
    user = await update_user_service(db, user_id, updates)  # Llama a la función correcta
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Eliminar un usuario
@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()
    return None

# Login de usuario
@router.post("/login")
async def login_user(user: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == user.username))
    db_user = result.scalars().first()

    if not db_user or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Devuelve un token simulado para este ejemplo (puedes implementar JWT más adelante)
    return {"success": True, "token": "JWT_TOKEN"}
