# -*- coding: utf-8 -*-
import uvloop
import aiohttp
import asyncio as aio
import asyncpg
import time
from colorama import Fore
from bs4 import BeautifulSoup as soup


async def get_page(episode_number: int, session: aiohttp.ClientSession):
    print(f"{Fore.LIGHTMAGENTA_EX} getting episode {episode_number}")
    url = f"https://talkpython.fm/{episode_number}"
    async with session.get(url=url) as response:
        return await response.text()


def get_title(html, episode):
    print(f"{Fore.GREEN} getting title from episode {episode}")
    grabbing_page = soup(html, "lxml")
    title = grabbing_page.find("h1")
    return "No title" if not title else title.text


async def main_coro():
    tasks = []
    conn = await asyncpg.connect("postgresql://async:Dexter89!@localhost/async_db")

    async with aiohttp.ClientSession() as session:
        for episode in range(100, 110):
            task = (episode, aio.create_task(get_page(episode, session)))
            tasks.append(task)

        for e, t in tasks:
            html = await t
            title = get_title(html, e)

            await conn.execute("""insert into talks_headers (title, episode) values ($1, $2)""", title, e)
            rows = await conn.fetch("""select * from talks_headers""")
            print(f"rows amount {len(rows)}")
    await conn.close()


if __name__ == '__main__':
    start = time.time()
    print(f"Started at {time.strftime('%X')}")
    uvloop.install()
    aio.run(main_coro())
    print(f"Finished at {time.strftime('%X')}, overall time is {time.time() - start}")
