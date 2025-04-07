# Atomic Habits - Трекер полезных привычек
## О проекте
Проект создан на основе книги Джеймса Клира «Атомные привычки» (2018), которая посвящена приобретению новых полезных привычек и искоренению старых плохих привычек. Трекер помогает пользователям формировать и отслеживать полезные привычки, получая уведомления через Telegram.
## Структура проекта
```
atomic-habits/
├── config/             # Основные настройки проекта
├── tracker/           # Приложение для управления привычками
├── users/            # Приложение для управления пользователями
└── manage.py        # Точка входа в приложение
```

## Технологии
- Python 3.13
- Django 5.1.7
- Django REST Framework
- Celery
- Redis
- PostgreSQL
- JWT для аутентификации
- Swagger для документации API
- Telegram Bot API для уведомлений
## Установка и запуск
### Предварительные требования
- Python 3.13+
- PostgreSQL
- Redis
- Poetry
### Установка зависимостей
```bash
  poetry install
```
### Настройка окружения
1. Создайте файл `.env` в корневой директории проекта
2. Добавьте необходимые переменные окружения:
```
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```
### Запуск
1. Примените миграции:
```bash
  python manage.py migrate
```
2. Запустите Redis:
```bash
  redis-server
```
3. Запустите Celery:
Для ОС Windows:
```bash
  celery -A config worker -l INFO -P eventlet
  celery -A config beat -l info
```
Для остальных ОС:
```bash
  celery -A config worker -l info
  celery -A config beat -l info
```
4. Запустите сервер разработки:
```bash
  python manage.py runserver
```

## API Endpoints
### Аутентификация
- `POST /users/register/` - Регистрация нового пользователя
- `POST /users/token/` - Получение JWT токена
- `POST /users/token/refresh/` - Обновление JWT токена
### Привычки
- `GET /habits/` - Получение списка привычек пользователя
- `POST /habits/` - Создание новой привычки
- `GET /habits/{id}/` - Получение информации о конкретной привычке
- `PUT /habits/{id}/` - Обновление привычки
- `DELETE /habits/{id}/` - Удаление привычки
### Документация API
- `GET /swagger/` - Swagger UI с полной документацией API
## Автор
Антонюк Евгений
GitHub: [@AntonyukEvgeniy](https://github.com/AntonyukEvgeniy)