# Makhachkala Backend

Backend API для сети ресторанов "Махачкала"

## Технологии

- Python 3.11
- FastAPI
- PostgreSQL 15
- SQLAlchemy
- Pydantic

## Установка и запуск

### С Docker (рекомендуется)

```bash
docker-compose up --build
```

API будет доступен на `http://localhost:8000`

### Без Docker

1. Установите PostgreSQL
2. Создайте базу данных `makhachkala`
3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4. Настройте `.env` файл:

```bash
cp .env.example .env
```

5. Запустите сервер:

```bash
uvicorn app.main:app --reload
```

## API Документация

После запуска откройте:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Меню
- `GET /api/menu` - Список блюд
- `GET /api/menu/{id}` - Детали блюда
- `GET /api/categories` - Категории

### Рестораны
- `GET /api/restaurants` - Список ресторанов
- `GET /api/restaurants/{id}` - Детали ресторана

## Seed данные

При первом запуске автоматически создаются:
- 3 категории (Шаурма, Напитки, Закуски)
- 10 блюд
- 3 ресторана в Минске

## Структура проекта

```
backend/
├── app/
│   ├── api/
│   │   └── routes/          # API маршруты
│   ├── core/                # Конфигурация
│   ├── models/              # SQLAlchemy модели
│   ├── schemas/             # Pydantic схемы
│   ├── crud/                # CRUD операции
│   ├── db/                  # База данных
│   └── main.py              # Entry point
├── tests/                   # Тесты
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

## Разработка

### Создание новой миграции

```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

### Запуск тестов

```bash
pytest
```

## Примеры запросов

### Получить все блюда

```bash
curl http://localhost:8000/api/menu
```

### Получить блюда категории

```bash
curl http://localhost:8000/api/menu?category_id=<uuid>
```

### Получить категории

```bash
curl http://localhost:8000/api/categories
```

### Получить рестораны

```bash
curl http://localhost:8000/api/restaurants
```

