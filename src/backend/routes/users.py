from sqlalchemy.future import select
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from typing import List
from uuid import UUID
from passlib.context import CryptContext
from datetime import timedelta
from backend.core.database import get_db
from backend.models.user import User
from backend.schemas.user import UserCreate, UserResponse, UserUpdate, UserLogin, Token
from backend.services.user_service import (
    update_user_service,
    authenticate_user,
    create_access_token,
)
from backend.core.config import ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/api/users", tags=["Users"])

# Crear un nuevo usuario
@router.post("/", response_model=Token, status_code=201)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.email == user.email)
    result = await db.execute(stmt)
    db_user = result.scalars().first()

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(user.password)
    new_user = User(username=user.username, email=user.email, password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # Generar el token JWT para el usuario recién registrado
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

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
    user = await update_user_service(db, user_id, updates)
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
@router.post("/login", response_model=Token)
async def login_user(user: UserLogin, db: AsyncSession = Depends(get_db)):
    authenticated_user = await authenticate_user(db, user.username, user.password)
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": authenticated_user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
