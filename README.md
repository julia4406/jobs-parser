Переглянути, що в кеші:
```
docker exec -it jobbot-redis-1 redis-cli SMEMBERS sent_job_url
```

Очистити кеш тільки для відправлених вакансій:
```
docker exec -it jobbot-redis-1 redis-cli DEL sent_job_url

```