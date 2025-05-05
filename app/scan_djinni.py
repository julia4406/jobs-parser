import time
from bs4 import BeautifulSoup

from app.auth_selenium import authenticate


driver = authenticate()

# def get_description(url):
#     response = requests.get(url=url, headers=HEADERS)
#     soup = BeautifulSoup(response.text, "html.parser")
#     paragraphs = soup.select_one(".b-typo.vacancy-section")
#     description = ""
#     if paragraphs:
#         description = paragraphs.get_text(separator="\n", strip=True)
#     return description


def get_djinni_jobs(urls: dict) -> list[dict]:
    jobs = []
    jobs_in_url = []
    for experience, url in urls.items():
        jobs_in_url = parse_djinni_jobs(url=url, experience=experience)
        if jobs_in_url:
            jobs.extend(jobs_in_url)
    return jobs


def parse_djinni_jobs(url: str, experience: str) -> list[dict]:
    driver.get(url=url)
    time.sleep(3)
    page_html = driver.page_source
    soup = BeautifulSoup(page_html, "html.parser")
    jobs_list = soup.select('.list-jobs li[id^="job-item"]')

    print(len(jobs_list))
    djinni_jobs = []

    # for el in soup.select(".list-jobs"):
    #     print(el.select_one(".job-item__title-link")).text.strip()
    #     job_tag = el.select_one(".vt")
    #     if job_tag:
    #         job_url = job_tag["href"]
    #         job_title = job_tag.text.strip()
    #         job_experience = experience
    #         job_date = el.select_one(".date").text.strip()
    #         job_offerer = el.select_one(".company").text.strip()
    #         description = get_description(job_url)
    #         djinni_jobs.append({
    #             "title": job_title,
    #             "experience": job_experience,
    #             "date": job_date,
    #             "company": job_offerer,
    #             "url": job_url,
    #             "description": description
    #         })
    driver.quit()

    return djinni_jobs


if __name__ == "__main__":
    print(get_djinni_jobs({
        "first_job": "https://djinni.co/jobs/?all_keywords=Python&exp_level=no_exp",
        # "under_1year": "https://djinni.co/jobs/?all_keywords=Python&exp_level=1y",
        # "2 years": "https://djinni.co/jobs/?all_keywords=Python&exp_level=2y"
    }))
