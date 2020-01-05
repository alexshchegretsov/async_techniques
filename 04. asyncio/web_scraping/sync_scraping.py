# -*- coding: utf-8 -*-
import requests
from colorama import Fore
from bs4 import BeautifulSoup as soup
from datetime import datetime

url = "https://talkpython.fm"


def get_page(episode_number: int):
    print(f"{Fore.LIGHTMAGENTA_EX} getting episode {episode_number}")
    r = requests.get(url=f"{url}/{episode_number}")
    r.episode = episode_number
    return r


def get_title(page):
    print(f"{Fore.GREEN} getting title from episode {page.episode}")
    grabbing_page = soup(page.text, "html.parser")
    title = grabbing_page.find("h1")
    return title.text if title else "No title"


def parse(_from, to):
    for i in range(_from, to):
        page = get_page(i)
        title = get_title(page)
        print(f"{Fore.CYAN} Title found: {title}\n")


def main():
    start = datetime.now()
    print(f"{Fore.YELLOW} Started at {start}")
    parse(150, 160)
    print(f"{Fore.RED} Overall time is {datetime.now() - start}")


if __name__ == '__main__':
    main()
