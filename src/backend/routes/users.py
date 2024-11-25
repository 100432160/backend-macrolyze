from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.database import get_db
from backend.models.user import User
from backend.schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Verificar si el usuario ya existe
    stmt = select(User).where(User.email == user.email)
    result = await db.execute(stmt)
    db_user = result.scalars().first()

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Crear el nuevo usuario
    new_user = User(
        username=user.username,
        email=user.email,
        password=user.password  # Asegúrate de hashear la contraseña si es necesario
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
