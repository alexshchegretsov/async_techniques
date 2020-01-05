# -*- coding: utf-8 -*-
import uvloop
import aiohttp
import asyncio as aio
import time
from colorama import Fore
from datetime import datetime
from bs4 import BeautifulSoup as soup


async def get_page(episode_number: int, session: aiohttp.ClientSession):
    print(f"{Fore.LIGHTMAGENTA_EX} getting episode {episode_number}")
    url = f"https://talkpython.fm/{episode_number}"
    async with session.get(url=url) as response:
        html = await response.text()
        get_title(html, episode_number)


def get_title(html, episode):
    print(f"{Fore.GREEN} getting title from episode {episode}")
    grabbing_page = soup(html, "html.parser")
    title = grabbing_page.find("h1")
    print(f"{title.text}\n")
    return "No title" if not title else title.text


async def main_coro():

    tasks = []
    async with aiohttp.ClientSession() as session:
        for episode in range(100, 130):
            task = aio.create_task(get_page(episode, session))
            tasks.append(task)
        await aio.gather(*tasks)


if __name__ == '__main__':
    start = time.time()
    print(f"Started at {time.strftime('%X')}")
    uvloop.install()
    aio.run(main_coro())
    print(f"Finished at {time.strftime('%X')}, overall time is {time.time() - start}")
