import asyncio

from queries.orm import AsyncORM

if __name__ == '__main__':
    asyncio.run(AsyncORM.create_tables())
    # asyncio.run(AsyncORM.insert_data())
