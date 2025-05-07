from datetime import datetime
import time
from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from app.urls import DJINNI_BASE


def get_description(url, driver):
    description = ""
    driver.get(url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    tag = soup.select_one(".job-post__description")
    if tag:
        description = tag.get_text(separator="\n", strip=True)

    return description


def parse_djinni_jobs(
        url: str, experience: str, driver
        ) -> list[dict]:
    driver.get(url=url)
    time.sleep(3)
    page_html = driver.page_source
    soup = BeautifulSoup(page_html, "html.parser")

    djinni_jobs = []

    jobs_list = soup.select('.list-jobs li[id^="job-item"]')

    for el in jobs_list:
        parse_job_url = el.select_one(".job-item__title-link")["href"]
        job_url = f"{DJINNI_BASE}{parse_job_url}"

        job_title = el.select_one(".job-item__title-link").text.strip()
        job_experience = experience
        parse_data = el.select("div.text-secondary span")
        for span in parse_data:
            if span.has_attr("data-original-title"):
                job_date = span["data-original-title"].split()[1]
            else:
                job_date = datetime.now()
        job_offerer = el.select_one(".text-body").text.strip()
        description = get_description(job_url, driver)
        djinni_jobs.append({
            "title": job_title,
            "experience": job_experience,
            "date": job_date,
            "company": job_offerer,
            "url": job_url,
            "description": description
        })

    return djinni_jobs


def get_djinni_jobs(urls: dict) -> list[dict]:
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        options=chrome_options
    )

    jobs = []
    jobs_in_url = []
    for experience, url in urls.items():
        jobs_in_url = parse_djinni_jobs(
            url=url, experience=experience, driver=driver
            )
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
