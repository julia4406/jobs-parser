import os
from dotenv import load_dotenv

import redis


load_dotenv()

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    db=0,
    decode_responses=True,
)

CACHE_KEY = "sent_job_url"


def is_parsed(job_url: str):
    return redis_client.sismember(CACHE_KEY, job_url)


def mark_as_parsed(job_url: str):
    redis_client.sadd(CACHE_KEY, job_url)
