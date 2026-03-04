# MindShare-API

## Запуск через Docker

1. Клонируйте репозиторий
2. `cp .env.sample .env` и отредактируйте
3. `docker-compose up -d`
4. Откройте `http://localhost:8000`

## Проверка сервисов
- `docker-compose ps` — все контейнеры должны быть Up
- `docker-compose logs -f web` — логи Django
- `docker-compose logs -f celery` — логи Celery
- `http://localhost:8000/admin` — админка

## Команды
- Остановка: `docker-compose down`
- Перезапуск: `docker-compose restart`
- Миграции: `docker-compose exec web python manage.py migrate`
- Суперпользователь: `docker-compose exec web python manage.py createsuperuser`
