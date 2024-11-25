from backend.models.user import Base  # Asegúrate de importar todos tus modelos
from backend.core.database import engine

async def init_db():
    async with engine.begin() as conn:
        print("Creating tables...")
        await conn.run_sync(Base.metadata.create_all)

# Si deseas ejecutarlo directamente:
if __name__ == "__main__":
    import asyncio
    asyncio.run(init_db())
