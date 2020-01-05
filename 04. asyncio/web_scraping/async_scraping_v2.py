# -*- coding: utf-8 -*-
import uvloop
import aiohttp
import asyncio as aio
import time
from colorama import Fore
from datetime import datetime
from bs4 import BeautifulSoup as soup


async def get_page(episode_number: int):
    print(f"{Fore.LIGHTMAGENTA_EX} getting episode {episode_number}")
    url = f"https://talkpython.fm/{episode_number}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as response:
            return await response.text()



def get_title(html, episode):
    print(f"{Fore.GREEN} getting title from episode {episode}")
    grabbing_page = soup(html, "html.parser")
    title = grabbing_page.find("h1")
    return "No title" if not title else title.text


async def main_coro():

    tasks = []

    for episode in range(100, 130):
        task = (episode ,aio.create_task( get_page(episode) ) )
        tasks.append(task)

    for episode, task in tasks:
        html = await task
        title = get_title(html, episode)
        print(f"{title}\n")


if __name__ == '__main__':
    start = time.time()
    print(f"Started at {time.strftime('%X')}")
    aio.run(main_coro())
    print(f"Finished at {time.strftime('%X')}, overall time is {time.time() - start}")
