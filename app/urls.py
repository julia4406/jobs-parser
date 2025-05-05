# DOU
DOU_BASE = "https://jobs.dou.ua"
URL_DOU_FIRST_JOB = f"{DOU_BASE}/first-job/?category=Python"
URL_DOU_UNDER_1_YEAR = f"{DOU_BASE}/vacancies/?category=Python&exp=0-1"
URL_DOU_1_3_YEARS = f"{DOU_BASE}/vacancies/?category=Python&exp=1-3"


LINKS_DOU = {
    "first_job": URL_DOU_FIRST_JOB,
    "under_1year": URL_DOU_UNDER_1_YEAR,
    "1-3 years": URL_DOU_1_3_YEARS
}

# DJINNI
DJINNI_BASE = "https://djinni.co/jobs"
URL_DJINNI_FIRST_JOB = f"{DJINNI_BASE}/?all_keywords=Python&exp_level=no_exp"
URL_DJINNI_UNDER_1_YEAR = f"{DJINNI_BASE}/?all_keywords=Python&exp_level=1y"
URL_DJINNI_2_YEARS = f"{DJINNI_BASE}/?all_keywords=Python&exp_level=2y"

LINKS_DJINNI = {
    "first_job": URL_DJINNI_FIRST_JOB,
    "under_1year": URL_DJINNI_UNDER_1_YEAR,
    "2 years": URL_DJINNI_2_YEARS
}
