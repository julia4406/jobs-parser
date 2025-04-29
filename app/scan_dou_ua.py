import json

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


URL_0 = "https://jobs.dou.ua/first-job/?from=exp"
URL_1 = "https://jobs.dou.ua/vacancies/?category=Python&exp=0-1"
URL_2 = "https://jobs.dou.ua/vacancies/?category=Python&exp=1-3"

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


def get_dou_jobs():
    response = requests.get(url=URL_1, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    dou_jobs = []

    for el in soup.select(".l-vacancy"):
        job_tag = el.select_one(".vt")
        if job_tag:
            job_url = job_tag["href"]
            job_title = job_tag.text.strip()
            job_date = el.select_one(".date").text.strip()
            description = get_description(job_url)
            dou_jobs.append({
                "title": job_title,
                "date": job_date,
                "url": job_url,
                "description": description
            })

    return dou_jobs

def save_to_json():
    data = get_dou_jobs()
    with open("jobs.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    print(save_to_json())
