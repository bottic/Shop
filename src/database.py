import asyncio

from sqlalchemy import create_engine, URL, text
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from config import settings


engine = create_engine(
    url=settings.DATABASE_URL_pymysql,
    echo=True,
    pool_size=10,
    max_overflow=10,
)
async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncmy,
    echo=False,
    pool_size=10,
    max_overflow=10,
)

session_factory = sessionmaker(engine)
async_session_factory = async_sessionmaker(async_engine)


class Base(DeclarativeBase):
    pass


# async def create_table():
#     async with engine.connect() as conn:
#         res = await conn.execute(text("SELECT VERSION()"))
#         print(res)

# asyncio.run(get())
