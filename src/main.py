import asyncio


from database.dtos import ProductPostDTO
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from queries.orm import AsyncORM, ProductORM
from decimal import Decimal


async def main():
    # await AsyncORM.create_tables()
    pass

#
def create_fastapi_app():
    app = FastAPI(title="FastAPI")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173"
        ],
        allow_credentials=True,  # Разрешаем куки и авторизацию
        allow_methods=["*"],  # Разрешаем все HTTP-методы
        allow_headers=["*"]  # Разрешаем все заголовки
    )

    @app.get("/products", tags=["Продукты"])
    async def get_resumes():
        resumes = await ProductORM.select_all_products()
        return resumes

    @app.post("/addProduct")
    async def add_product(product_data: ProductPostDTO):  # Используем DTO как тип параметра
        new_product = await ProductORM.insert_product(product_data)
        return new_product

    @app.delete("/deleteProduct")
    async def delete_product(sku):
        result = await ProductORM.delete_product_by_sku(sku)
        return result

    return app

app = create_fastapi_app()

if __name__ == '__main__':
    asyncio.run(main())
    uvicorn.run(
        app="src.main:app",
        reload=True,
    )
    # print(a[0])
    # asyncio.run(AsyncORM.insert_data())
