# MindShare-API (DRF)

Проект представляет собой REST API для платформы обмена знаниями. Реализована аутентификация по JWT, 
управление курсами и уроками, интеграция с платежной системой Stripe и фоновые задачи через Celery.

## Стек технологий

- **Django** & **Django REST Framework** (DRF)
- **PostgreSQL** (основная БД) / **SQLite** (для тестов и упрощенного деплоя)
- **Celery** & **Redis** (фоновые задачи)
- **Docker** & **Docker Compose** (контейнеризация)
- **GitHub Actions** (CI/CD)

## Настройка удаленного сервера

Для работы проекта был создан виртуальный сервер в **Yandex Cloud** со следующими характеристиками:
- **ОС:** Ubuntu 22.04
- **vCPU:** 2
- **RAM:** 2 ГБ
- **Диск:** HDD 20 ГБ
- **Публичный IP:** динамический

### Подготовка сервера (выполняется вручную при первом развертывании):

1. Подключиться к серверу по SSH.
2. Установить Docker и Docker Compose:
   ```bash
   sudo apt update && sudo apt install docker.io docker-compose -y
   sudo usermod -aG docker $USER

## GitHub Actions CI/CD

Workflow настроен на автоматическую сборку и деплой при каждом push в ветку feature/* или develop.

## Процесс CI/CD:

1.Линтинг (flake8) — проверка качества кода.
2.Тестирование — запуск тестов Django с временным SECRET_KEY.
3.Сборка Docker-образа — на основе Dockerfile.
4.Публикация в Docker Hub — образ отправляется в репозиторий mindshare-api.
5.Деплой на сервер — через SSH (или пароль) на ВМ в Yandex Cloud.

## Переменные окружения (Secrets), необходимые для работы:

DJANGO_SECRET_KEY         Секретный ключ Django
DOCKER_HUB_ACCESS_TOKEN   Токен доступа Docker Hub
DOCKER_HUB_USERNAME       Логин Docker Hub
SERVER_IP_FINAL           Публичный IP сервера
SSH_KEY_FINAL             Ключ(приватный) для подключения к серверу
SSH_USER                  Имя пользователя на сервере
  
## Локальный запуск проекта

1.Клонировать репозиторий:

    git clone git@github.com:LeeVed/MindShare-API.git
    cd MindShare-API

2.Создать файл .env по примеру .env.example.

3.Запустить проект с помощью Docker Compose:

    docker-compose up

4.Приложение будет доступно по адресу http://localhost:8000.

## Документация API

После запуска проекта документация доступна по адресу /swagger/ или /redoc/.

## Примечание

Для работы фоновых задач (Celery) необходимо запускать отдельные контейнеры celery и celery-beat, 
что уже настроено в docker-compose.yml.
