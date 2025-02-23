

from sqlalchemy import insert, select
from src.database import engine, async_engine, session_factory, async_session_factory
from src.dtos import ProductGetDTO
from src.models import Base, UserTable, ProductTable, CategoryTable
from sqlalchemy.orm import selectinload
from decimal import Decimal

class AsyncORM:
    @staticmethod
    async def create_tables():
        async_engine.echo = False

        async with async_engine.begin() as conn:
            # Асинхронное выполнение через run_sync()

            # await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        async_engine.echo = True
        await async_engine.dispose()

    @staticmethod
    async def insert_user():
        async with async_session_factory() as session:
            product = UserTable(email='one', password_hash='onedesc')
            session.add(product)
            await session.commit()




class ProductORM:
    @staticmethod
    async def select_all_products():
        async with async_session_factory() as session:
            query = select(ProductTable)
            result = await session.execute(query)
            products = result.scalars().all()
            products_dto = [ProductGetDTO.model_validate(row, from_attributes=True) for row in products]
            return products_dto

    # @staticmethod
    # async def select_one_products(id:int):
    #     async with async_session_factory() as session:
    #         result = await session.get(ProductTable, id)
    #         product = result.scalars()
    #         return product


    @staticmethod
    async def insert_product(
            title: str,
            description: str,
            price: float,
            sku: str,
            categories: list[int] | None = None  # список ID категорий (опционально)
    ):
        async with async_session_factory() as session:
            # Создаем базовый объект продукта
            product = ProductTable(
                title=title,
                description=description,
                price=price,
                sku=sku
            )

            # Добавляем категории, если они указаны
            if categories:
                # Получаем категории из базы
                result = await session.execute(
                    select(CategoryTable).where(CategoryTable.id.in_(categories))
                )
                categories_objs = result.scalars().all()

                # Добавляем связи с категориями
                product.categories.extend(categories_objs)

            session.add(product)
            await session.commit()
            await session.refresh(product)  # Обновляем объект с данными из БД

            # Возвращаем созданный продукт с категориями
            return await session.get(
                ProductTable,
                product.id,
                options=[selectinload(ProductTable.categories)]
            )
