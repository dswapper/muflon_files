# Файлы Муфлона

[![Python](https://img.shields.io/badge/python-3.10-blue?logo=python&logoColor=white)](https://www.python.org/) 
[![Aiogram](https://img.shields.io/badge/aiogram-3.0-blue?logo=python&logoColor=white)](https://docs.aiogram.dev/) 
[![Docker](https://img.shields.io/badge/docker-20.10-blue?logo=docker&logoColor=white)](https://www.docker.com/)

**Файлы Муфлона** — шуточный телеграм-бот, который маскирует сообщения символами █, кроме слова **Муфлон** и его производных.

## Быстрый старт

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/dswapper/muflon_files.git
cd muflon_files
```

### 2. Создайте .env файл на основе .env.example с вашим токеном бота

Обязательные измените следующие поля в .env.example. **Не используйте** в паролях спецсимволы.
```bash
BOT_TOKEN=<ваш_токен>
POSTGRES_PASSWORD=<ваш_пароль>
REDIS_PASSWORD=<ваш_пароль>
```

### 3. Запускайте бота
```bash
docker compose -f docker-compose.prod.yml -f docker-compose.yml up -d
```

## Старт из fork'а

### 1. Создайте форк репозитория

### 2. Создайте в github окружение production

1. Перейдите в Settings → Environments
2. Создайте окружение с именем **production**


### 3. Настройте ваш сервер

1. Установите docker
```bash
sudo apt update
sudo apt install -y docker.io docker-compose-plugin
sudo systemctl enable docker
sudo systemctl start docker
```

2. Создайте пользователя для деплоя и дайте ему доступ к docker
```bash
sudo adduser deploy
sudo usermod -aG docker deploy
```

3. Создайте ssh ключ для подключения к серверу

На **локальной машине**:
```bash
ssh-keygen -t ed25519 -f ~/.ssh/deploy_key -C "github-actions"
```

На сервере:
```bash
su - deploy
mkdir -p ~/.ssh
chmod 700 ~/.ssh
nano ~/.ssh/authorized_keys
```
Вставь содержимое deploy_key.pub, затем проверка:
```bash
ssh -i ~/.ssh/deploy_key deploy@<SERVER_IP>
```

### 4. Внесите в окружение следующие значения
Перейдите в:
Repository → Settings → Environments → production → Secrets

Добавьте следующие значения Secrets:
```bash
# Токен бота API Telegram
BOT_TOKEN
# Postgres
POSTGRES_DB 
POSTGRES_HOST
POSTGRES_PASSWORD
POSTGRES_PORT
POSTGRES_USER
# Redis
REDIS_HOST
REDIS_PASSWORD
REDIS_PORT
# SHH к вашему серверу
SSH_HOST - ip сервера
SSH_USER - user с docker группой на сервере
SSH_PRIVATE_KEY
```
Добавьте следующие значения в variables:
```bash
GHCR_IMAGE = ghcr.io/dswapper/muflon_files
```

## 5. Первый деплой

Вариант 1. Деплой по тегу (рекомендуется)

Вы можете запустить деплой, создав git-тег вида ```v*.*.*```:
```bash
git tag <tag:v*.*.*>
git push origin <tag:v*.*.*>
```

Вариант 2. Ручной запуск деплоя
1. Перейдите во вкладку Actions
2. Откройте workflow Build & Deploy
3. Нажмите Run workflow
4. Выберите ветку main
5. Запустите workflow

