# Task Manager API

REST API для управления задачами с JWT авторизацией.

## Технологии

- **FastAPI** — веб-фреймворк
- **SQLAlchemy** — ORM для работы с базой данных
- **SQLite** — база данных
- **JWT** — авторизация
- **pytest** — тестирование
- **Docker** — контейнеризация

## Запуск через Docker

```bash
docker-compose up --build
```

API будет доступен на http://localhost:8000

Документация: http://localhost:8000/docs

## Запуск локально

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Эндпоинты

### Авторизация
| Метод | URL | Описание |
|-------|-----|----------|
| POST | /api/v1/auth/register | Регистрация |
| POST | /api/v1/auth/login | Вход, получение токена |

### Задачи (требуют авторизации)
| Метод | URL | Описание |
|-------|-----|----------|
| GET | /api/v1/tasks/ | Список задач |
| POST | /api/v1/tasks/ | Создать задачу |
| GET | /api/v1/tasks/{id} | Получить задачу |
| PATCH | /api/v1/tasks/{id} | Обновить задачу |
| DELETE | /api/v1/tasks/{id} | Удалить задачу |

## Тесты

```bash
pytest -v
```

12 тестов, покрывают авторизацию, CRUD и права доступа.