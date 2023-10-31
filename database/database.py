from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URL = "sqlite+aiosqlite:///./legadrop.db"
engine = create_async_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

@asynccontextmanager
async def get_session():
    session = SessionLocal()
    try:
        yield session
    except Exception as e:
        print(e)
        await session.rollback()
        raise e
    finally:
        await session.close()
