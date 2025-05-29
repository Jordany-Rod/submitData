# FSTR API — Сервис для учета горных перевалов

## О проекте

REST API для сбора и систематизации данных о горных перевалах в рамках сотрудничества
с Федерацией спортивного туризма России (ФСТР). Сервис позволяет:

- Добавлять новые перевалы через POST-запросы
- Получать списки перевалов по email пользователя
- Просматривать детальную информацию о конкретном перевале
- Редактировать данные (только для перевалов со статусом "new")

Автоматически генерируемая документация доступна через Swagger UI и ReDoc.

## Технологический стек

- Python 3.8
- Django 4.2.21 + Django REST Framework
- PostgreSQL (с драйвером psycopg2-binary)
- drf-yasg — генерация OpenAPI-документации
- django-filter — фильтрация данных в API
- python-dotenv — управление конфигурацией

## Структура проекта

- 'pereval/submitData/models.py' - Модели данных (пользователи, перевалы, координаты)
- 'pereval/submitData/serializers.py' - Сериализаторы для API
- 'pereval/submitData/views.py' - Логика обработки запросов
- 'pereval/submitData/urls.py' - Маршруты приложения
- 'pereval/submitData/resources.py' - Вынесены статусы модерации в отдельный файл
- 'pereval/pereval/settings.py' - Конфигурация проекта c подключением к .env
- 'pereval/pereval/urls.py' - Корневые маршруты

## Установка и запуск проекта

1. Клонировать репозиторий:
```bash
git clone https://github.com/Jordany-Rod/submitData.git
cd submitData
```
2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/macOS
venv\Scripts\activate   # для Windows
```
3. Настройка БД (создайте базу в PostgreSQL)


4. Создайте файл .env в корневой директории проекта pereval/ (на одном уровне с settings.py) и заполните его следующими данными:
```ini
FSTR_DB_NAME=your_db_name  # имя БД
FSTR_DB_LOGIN=your_db_user  # имя пользователя
FSTR_DB_PASS=your_db_password  # пароль
FSTR_DB_HOST=localhost
FSTR_DB_PORT=port # Обычно порт для PostgreSQL — 5432
```
5. Применить миграции и запустить сервер:
```bash
python manage.py migrate
python manage.py runserver
```
## Документация API

После запуска сервера документация доступна по адресам:

- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

## Основные эндпоинты

- POST   `/api/submitData/` - Добавить новый перевал
- GET    `/api/submitData/?user__email=example@mail.ru` - Получить список перевалов по email 
- GET    `/api/submitData/<id>/` - Получить информацию о перевале по ID 
- PATCH  `/api/submitData/<id>/` - Обновить перевал (если status = "new") 

## Пример запроса

```json
        {
            "beauty_title": "пер.",
            "title": "Дятлова",
            "other_titles": "Холатчахль",
            "connect": "",
            "add_time": "2021-09-22 13:18:13",
            "user": {
                "email": "qwerty@mail.ru",
                "fam": "Пупкин",
                "name": "Василий",
                "otc": "Иванович",
                "phone": "+7 555 55 55"
            },
            "coords": {
                "latitude": "45.3842",
                "longitude": "7.1525",
                "height": "1096"
            },
            "level": {
                "winter": "",
                "summer": "1А",
                "autumn": "1А",
                "spring": ""
            },
            "images": [
                {"title": "Седловина", "image_url": "http://example.com/image1.jpg"},
                {"title": "Подъем", "image_url": "http://example.com/image2.jpg"}
            ]
        }
```
## Ограничения

1. Редактирование возможно только для перевалов со статусом "new"
2. Для создания перевала требуется существующий или вновь создаваемый пользователь

## Контакты

Разработчик: Егор Родионов

Email: erop1997@mail.ru

Организация: ФСТР (Федерация спортивного туризма России)

---
Проект разработан в рамках учебной программы SkillFactory.