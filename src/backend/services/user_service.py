from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.user import User
from backend.schemas.user import UserCreate, UserUpdate
from passlib.context import CryptContext
from uuid import UUID
from datetime import datetime, timedelta, timezone
import jwt
from backend.core.config import SECRET_KEY, ALGORITHM
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Crear un nuevo usuario
async def create_user(db: AsyncSession, user: UserCreate):
    result = await db.execute(select(User).where(User.email == user.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(user.password)
    new_user = User(username=user.username, email=user.email, password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

# Obtener todos los usuarios
async def get_all_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()

# Obtener un usuario por ID
async def get_user_by_id(db: AsyncSession, user_id: UUID):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().first()

# Actualizar un usuario
async def update_user_service(db: AsyncSession, user_id: UUID, updates: UserUpdate):
    user = await get_user_by_id(db, user_id)
    if not user:
        return None

    if updates.username:
        user.username = updates.username
    if updates.password:
        user.password = pwd_context.hash(updates.password)

    await db.commit()
    await db.refresh(user)
    return user

# Eliminar un usuario
async def delete_user(db: AsyncSession, user_id: UUID):
    user = await get_user_by_id(db, user_id)
    if not user:
        return None

    await db.delete(user)
    await db.commit()
    return user

# Autenticar un usuario (login)
async def authenticate_user(db: AsyncSession, username: str, password: str):
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()

    if user and pwd_context.verify(password, user.password):
        return user
    return None

# Crear un token JWT
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
