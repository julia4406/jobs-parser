import os

import redis

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True,
)

CACHE_KEY = "sent_job_url"

def is_sent(job_url: str):
    return redis_client.sismember(CACHE_KEY, job_url)


def mark_as_sent(job_url: str):
    redis_client.sadd(CACHE_KEY, job_url)
