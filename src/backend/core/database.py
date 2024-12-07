from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./macrolyze.db"  # Cambia según tu configuración
# DATABASE_URL = "sqlite:///./macrolyze.db"  # Cambia según tu configuración

engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()  # Define un único Base

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    async with async_session() as session:
        yield session
