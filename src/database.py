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
    echo=True,
    pool_size=10,
    max_overflow=10,
)

session_factory = sessionmaker(engine)
async_session_factory = async_sessionmaker(async_engine)


class Base(DeclarativeBase):
    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        """Relationships не используются в repr(), т.к. могут вести к неожиданным подгрузкам"""
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


# async def create_table():
#     async with engine.connect() as conn:
#         res = await conn.execute(text("SELECT VERSION()"))
#         print(res)

# asyncio.run(get())
