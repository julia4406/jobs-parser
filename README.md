Переглянути, що в кеші:
```
docker exec -it jobbot-redis-1 redis-cli SMEMBERS sent_job_url
```

Очистити кеш тільки для відправлених вакансій:
```
docker exec -it jobbot-redis-1 redis-cli DEL sent_job_url

```
docker-compose.override.yml
Цей файл автоматично підхоплюється при запуску:

docker-compose up --build

✅ 2. У проді не використовуй starter:

Запускай через:

docker-compose -f docker-compose.yml up --build