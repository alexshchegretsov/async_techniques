# -*- coding: utf-8 -*-
import requests
import time
import psycopg2
from bs4 import BeautifulSoup
from http_request_randomizer.requests.useragent.userAgent import UserAgentManager as agent

JOOBLE_URL = "https://by.jooble.org/вакансии-{}/Минск"
query = "python"

headers = {
    "Accept": "text/css,*/*;q=0.1",
    "User-Agent": agent().get_random_user_agent(),
}


def get_response(session: requests.Session, url: str):
    with session.get(url=url, headers=headers) as response:
        return response


def get_page_amount(response):
    soup = BeautifulSoup(response.content, "lxml")
    pagination = soup.find("div", attrs={"class": "paging"})
    page_amount = int(pagination.find_all("a")[-1].text) if pagination else 1
    return page_amount


def get_all_urls(page_amount: int, request_url: str):
    urls_to_processing = []
    for page_number in range(1, page_amount + 1):
        url = f"{request_url}&p={page_number}"
        urls_to_processing.append(url)
    return urls_to_processing


def parse_pages(response, new_vacancies: list):
    soup = BeautifulSoup(response.content, "lxml")
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


def main():
    conn = psycopg2.connect(user="async",
                            password="Dexter89!",
                            host="127.0.0.1",
                            port="5432",
                            database="async_parser")
    cursor = conn.cursor()
    formula = """insert into jobs(title, company, href, description, date_add) values (%s, %s, %s, %s, %s) """
    new_vacancies = []
    url = JOOBLE_URL.format(query)
    with requests.Session() as session:
        response = get_response(session, url)
        pages = get_page_amount(response)
        urls_to_processing = get_all_urls(pages, url)

        for url in urls_to_processing:
            resp = get_response(session, url)
            # produce tasks
            parse_pages(resp, new_vacancies)
            # process tasks
            while new_vacancies:
                to_db = new_vacancies.pop(0)
                record_to_insert = to_db["title"], to_db["company"], to_db["href"], to_db["short_description"], to_db[
                    "date_add"]
                cursor.execute(formula, record_to_insert)
        conn.commit()
        cursor.close()
        conn.close()


if __name__ == '__main__':
    start = time.time()
    print(f"Started at {time.strftime('%X')}")
    main()
    print(f"Finished at {time.strftime('%X')}, overall time is {time.time() - start}")
