# Hop & Barley - Интернет-магазин ингредиентов для пивоварения

Проект выполнен в рамках учебного курса. Представляет собой полноценный интернет-магазин с Web-интерфейсом и REST API.

## Технологии
- **Backend:** Django 5.2, DRF
- **Database:** PostgreSQL
- **Infrastructure:** Docker, Docker Compose
- **Quality:** Pytest, Flake8, Mypy
- **Auth:** JWT (SimpleJWT)

## Запуск проекта
0. Клонируйте репозиторий:
1. Создайте файл `.env` на основе `.env.example`
2. Запустите контейнеры:
   ```bash
   docker-compose up --build
   ```

Создайте суперпользователя:
   ```bash
    docker-compose exec web python manage.py createsuperuser
   ```

Документация API
После запуска документация доступна по адресу: http://127.0.0.1:8000/api/docs/

Тестирование и Линтеры
Запуск тестов: pytest
Проверка кода: 
   ```bash
    flake8 .
    mypy .
   ```

### Что сделать сейчас:
1. Создай файлы `.flake8` и `pytest.ini`.
2. Обнови `settings.py` и `urls.py` для Swagger.
3. Запусти `pytest` и убедись, что тест проходит.
4. Открой Swagger и проверь, что он видит твои `Product` и `Order`.

**Если возникнут проблемы с импортами в тестах или Docker-контейнером — пиши!** Ты на финишной прямой.
