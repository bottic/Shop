

from sqlalchemy import select
from src.database.database import async_engine, async_session_factory
from src.database.dtos import ProductGetDTO, ProductPostDTO, CategoryGetDTO
from src.database.models import Base, UserTable, ProductTable, CategoryTable
from sqlalchemy.orm import selectinload, joinedload


class AsyncORM:
    # @staticmethod
    # async def create_tables():
    #     async_engine.echo = False
    #
    #     async with async_engine.begin() as conn:
    #         # Асинхронное выполнение через run_sync()
    #
    #         await conn.run_sync(Base.metadata.drop_all)
    #         await conn.run_sync(Base.metadata.create_all)
    #     async_engine.echo = True
    #     await async_engine.dispose()

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
            # Явно загружаем категории
            query = select(ProductTable).options(
                selectinload(ProductTable.categories))

            result = await session.execute(query)
            products = result.scalars().all()

            return [
                ProductGetDTO(
                    id=product.id,
                    title=product.title,
                    description=product.description,
                    price=float(product.price),  # Конвертация
                    sku=product.sku,
                    categories=[
                        CategoryGetDTO(id=c.id, name=c.name)
                        for c in product.categories
                    ],
                    created_at=product.created_at,
                    updated_at=product.updated_at
                ) for product in products
            ]

    @staticmethod
    async def select_one_products(id:int):
        async with async_session_factory() as session:
            result = await session.get(ProductTable, id)
            product = result.scalars()
            return product

    @staticmethod
    async def insert_product(product_data: ProductPostDTO):
        async with async_session_factory() as session:
            # Создаем объект продукта
            product = ProductTable(
                title=product_data.title,
                description=product_data.description,
                price=product_data.price,
                sku=product_data.sku,
            )

            # Добавляем категории, если они указаны
            if product_data.categories:
                result = await session.execute(
                    select(CategoryTable).where(CategoryTable.id.in_(product_data.categories))
                )
                categories = result.scalars().all()
                product.categories.extend(categories)

            # Сохраняем продукт в базу данных
            session.add(product)
            await session.commit()
            await session.refresh(product)

            return product

    @staticmethod
    async def delete_product_by_sku(sku: str):
        async with async_session_factory() as session:
            # Находим продукт по SKU
            result = await session.execute(
                select(ProductTable).where(ProductTable.sku == sku)
            )
            product = result.scalars().first()

            # Проверяем, найден ли продукт
            if product:
                # Удаляем продукт
                await session.delete(product)
                await session.commit()
                return {"message": "Продукт успешно удален"}
            else:
                return {"message": "Продукт с указанным SKU не найден"}
