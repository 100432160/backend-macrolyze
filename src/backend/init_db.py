from backend.models import *  # Importa todos los modelos para registrarlos
from backend.core.database import Base, engine

async def init_db():
    async with engine.begin() as conn:
        print("Dropping all tables...")
        await conn.run_sync(Base.metadata.drop_all)
        print("Registered tables before create_all:", Base.metadata.tables.keys())
        print("Creating tables...")
        await conn.run_sync(Base.metadata.create_all)
        print("Registered tables after create_all:", Base.metadata.tables.keys())

if __name__ == "__main__":
    import asyncio
    asyncio.run(init_db())
