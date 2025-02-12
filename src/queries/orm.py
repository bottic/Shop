from sqlalchemy import insert
from src.database import engine, async_engine, session_factory, async_session_factory
from src.models import Base, UserOrm

class AsyncORM():
    @staticmethod
    async def create_tables():
        async_engine.echo = False

        async with async_engine.begin() as conn:
            # Асинхронное выполнение через run_sync()
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

        await async_engine.dispose()

    @staticmethod
    async def insert_data():
        async with async_session_factory() as session:
            product = UserOrm(email='one', password_hash='onedesc')
            session.add(product)
            await session.commit()

