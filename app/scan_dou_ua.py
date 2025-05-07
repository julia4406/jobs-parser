import json

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from app.cache_checker import is_parsed, mark_as_parsed

ua = UserAgent()
HEADERS = {"user-agent": ua.random}

ua = UserAgent()


def get_description(url):
    response = requests.get(url=url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = soup.select_one(".b-typo.vacancy-section")
    description = ""
    if paragraphs:
        description = paragraphs.get_text(separator="\n", strip=True)
    return description


def get_dou_jobs(urls: dict) -> list[dict]:
    jobs = []
    jobs_in_url = []
    for experience, url in urls.items():
        jobs_in_url = parse_dou_jobs(url=url, experience=experience)
        if jobs_in_url:
            jobs.extend(jobs_in_url)
    return jobs


def parse_dou_jobs(url: str, experience: str) -> list[dict]:
    response = requests.get(url=url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    dou_jobs = []

    for el in soup.select(".l-vacancy"):
        job_tag = el.select_one(".vt")
        if job_tag:
            job_url = job_tag["href"]
            if is_parsed(job_url):
                break
            job_title = job_tag.text.strip()
            job_experience = experience
            job_date = el.select_one(".date").text.strip()
            job_offerer = el.select_one(".company").text.strip()
            description = get_description(job_url)
            dou_jobs.append({
                "title": job_title,
                "experience": job_experience,
                "date": job_date,
                "company": job_offerer,
                "url": job_url,
                "description": description
            })
            mark_as_parsed(job_url)
    return dou_jobs


def save_to_json():
    data = get_dou_jobs()
    with open("jobs.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    print(save_to_json())
