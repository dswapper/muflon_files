# Файлы Муфлона

[![Python](https://img.shields.io/badge/python-3.10-blue?logo=python&logoColor=white)](https://www.python.org/) 
[![Aiogram](https://img.shields.io/badge/aiogram-3.0-blue?logo=python&logoColor=white)](https://docs.aiogram.dev/) 
[![Docker](https://img.shields.io/badge/docker-20.10-blue?logo=docker&logoColor=white)](https://www.docker.com/)

**Файлы Муфлона** — шуточный телеграм-бот, который маскирует сообщения символами █, кроме слова **Муфлон** и его производных.

## Быстрый старт

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/dswapper/muflon_files.git
cd muflon-files-bot
```

### 2. Создайте .env файл с вашим токеном бота

```bash
BOT_TOKEN=<ваш_токен>
```

### 3. Соберите Docker-образ

```bash
docker build -t muflon_bot .
```

### 4. Запустите контейнер

```bash
docker run -d --env-file .env --name muflon_bot muflon_bot
```