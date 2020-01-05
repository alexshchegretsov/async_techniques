# -*- coding: utf-8 -*-
import aiohttp
import uvloop
import asyncio
import requests
import asyncpg
from bs4 import BeautifulSoup
from http_request_randomizer.requests.useragent.userAgent import UserAgentManager as agent
import time

JOOBLE_URL = "https://by.jooble.org/вакансии-{}/Минск"
query = "python"

headers = {
    "Accept": "text/css,*/*;q=0.1",
    "User-Agent": agent().get_random_user_agent(),
}


async def get_response(session: aiohttp.ClientSession, url: str):
    async with session.get(url=url, headers=headers) as response:
        return await response.text()


def define_pages_amount(response_html):
    soup = BeautifulSoup(response_html, "lxml")
    pagination = soup.find("div", attrs={"class": "paging"})
    page_amount = int(pagination.find_all("a")[-1].text) if pagination else 1
    return page_amount


def get_all_urls(page_amount: int, request_url: str):
    urls_to_processing = []
    for page_number in range(1, page_amount + 1):
        url = f"{request_url}&p={page_number}"
        urls_to_processing.append(url)
    return urls_to_processing


def parse_page(response_html, new_vacancies: list):
    soup = BeautifulSoup(response_html, "lxml")
    divs = soup.find_all("div", attrs={"class": "result saved paddings"})
    for div in divs:
        title = div.find("h2", class_="position").text.strip()
        company = div.find("span", class_="gray_text company-name").text
        href = div.find("a", class_="link-position job-marker-js")["href"]
        short_descr = div.find("span", class_="description").text
        date_add = div.find("span", class_="date_location").text
        new_vacancies.append({
            "title": title,
            "company": company,
            "href": href,
            "short_description": short_descr,
            "date_add": date_add,
        })


async def main():
    db_conn = await asyncpg.connect("postgresql://async:Dexter89!@localhost/async_parser")
    url = JOOBLE_URL.format(query)
    new_vacancies = []
    tasks = []
    async with aiohttp.ClientSession() as session:
        response_html = requests.get(url).content
        pages = define_pages_amount(response_html)
        urls_to_processing = get_all_urls(pages, url)
        # produce tasks
        for url in urls_to_processing:
            task = asyncio.create_task(get_response(session, url))
            tasks.append(task)
        # process tasks
        for task in tasks:
            html = await task
            # produce tasks
            parse_page(html, new_vacancies)
            # process tasks
            while new_vacancies:
                to_db = new_vacancies.pop(0)
                await db_conn.execute(
                    """insert into jobs(title, company, href, description, date_add) values($1, $2, $3, $4, $5) """,
                    to_db["title"], to_db["company"], to_db["href"], to_db["short_description"], to_db["date_add"])
        # print(new_vacancies)
        await db_conn.close()


if __name__ == '__main__':
    start = time.time()
    print(f"Started at {time.strftime('%X')}")
    uvloop.install()
    asyncio.run(main())
    print(f"Finished at {time.strftime('%X')}, overall time is {time.time() - start}")
