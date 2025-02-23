import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from queries.orm import AsyncORM, ProductORM
from decimal import Decimal


async def main():
    await AsyncORM.create_tables()
    await ProductORM.insert_product('new', 'newdesc', float(1), '2', [])

#
def create_fastapi_app():
    app = FastAPI(title="FastAPI")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
    )

    @app.get("/products", tags=["Продукты"])
    async def get_resumes():
        resumes = await ProductORM.select_all_products()
        return resumes

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
