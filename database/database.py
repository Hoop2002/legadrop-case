from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://postgres@localhost/legadrop"
)


engine = create_async_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
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


DB_SYNC = os.getenv(
    "DATABASE_URL_PS", "postgresql+psycopg2://postgres@localhost/legadrop"
)
engine_sync = create_engine(DB_SYNC)

SessionLocalSync = sessionmaker(autocommit=False, autoflush=False, bind=engine_sync)


def get_sync_session():
    session = SessionLocalSync()
    session.begin()
    try:
        yield session
    except Exception as e:
        print(e)
        session.rollback()
        raise e
    finally:
        session.close()
