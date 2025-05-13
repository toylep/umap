from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from config.settings import Settings

db_settings = Settings.db
DATABASE_URL = f"postgresql+asyncpg://{db_settings.postgres_user}:{db_settings.postgres_password}@{db_settings.db_host}:5432/{db_settings.postgres_db}"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
