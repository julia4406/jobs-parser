import time
from bs4 import BeautifulSoup, Tag
import requests

from app.auth_selenium import authenticate
from app.bot import message_to_telegram
from app.cache_checker import is_parsed, mark_as_parsed
from app.urls import DJINNI_BASE


driver = authenticate()


def get_description(url):
    description = ""
    response = requests.get(url=url)
    time.sleep(5)
    soup = BeautifulSoup(response.text, "html.parser")
    tag = soup.select_one(".job-post__description")
    if tag:
        description = tag.get_text(separator="\n", strip=True)

    return description


def get_number_of_pages(url: str):
    driver.get(url=url)
    time.sleep(10)
    page_html = driver.page_source
    soup = BeautifulSoup(page_html, "html.parser")

    number_of_pages = 1
    if soup.select(".pagination"):
        number_of_pages = soup.select(
                ".pagination li.page-item"
                )[-2].text.strip()
    return int(number_of_pages)


def parse_djinni_jobs(url: str, experience: str) -> list[dict]:
    number_of_pages = get_number_of_pages(url)

    djinni_jobs = []
    stop_parse = False

    for page in range(1, number_of_pages + 1):
        page_url = f"{url}&page={page}"

        driver.get(url=page_url)
        time.sleep(10)

        page_html = driver.page_source
        soup = BeautifulSoup(page_html, "html.parser")

        jobs_list = soup.select('.list-jobs li[id^="job-item"]')

        if stop_parse:
            break

        for el in jobs_list:
            parse_job_url = el.select_one(".job-item__title-link")["href"]
            job_url = f"{DJINNI_BASE}{parse_job_url}"

            if is_parsed(job_url):
                stop_parse = True
                break

            job_title = el.select_one(".job-item__title-link").text.strip()
            job_experience = experience
            parse_data = el.select("div.text-secondary span")
            for span in parse_data:
                if span.has_attr("data-original-title"):
                    job_date = span["data-original-title"].split()[1]
            job_offerer = el.select_one(".text-body").text.strip()
            description = get_description(job_url)
            djinni_jobs.append({
                "title": job_title,
                "experience": job_experience,
                "date": job_date,
                "company": job_offerer,
                "url": job_url,
                "description": description
            })

            mark_as_parsed(job_url)

    # driver.quit()

    return djinni_jobs


def get_djinni_jobs(urls: dict) -> list[dict]:
    jobs = []
    jobs_in_url = []
    for experience, url in urls.items():
        jobs_in_url = parse_djinni_jobs(url=url, experience=experience)
        if jobs_in_url:
            jobs.extend(jobs_in_url)
    driver.quit()
    return jobs


if __name__ == "__main__":
    jobs = get_djinni_jobs({
        "first_job": f"{DJINNI_BASE}/jobs/?all_keywords=Python&exp_level=no_exp",
        # "under_1year": "https://djinni.co/jobs/?all_keywords=Python&exp_level=1y",
        # "2 years": "https://djinni.co/jobs/?all_keywords=Python&exp_level=2y"
    })
    print("total: ", jobs)
    for job in jobs:
        print(job["title"], " ", job["experience"])
