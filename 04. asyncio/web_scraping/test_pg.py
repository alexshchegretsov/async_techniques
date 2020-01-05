# -*- coding: utf-8 -*-
import asyncio
import asyncpg


async def run():
    # conn = await asyncpg.connect(user="async", password="Dexter89!", database="async_db", host="127.0.0.1", port="5432")
    conn = await asyncpg.connect("postgresql://async:Dexter89!@localhost/async_db")
    values = await conn.fetch("""select * from talks_headers""")
    await conn.close()
    print(values, len(values))

if __name__ == '__main__':
    asyncio.run(run())