Асинхронный микросервис для обработки платежей с поддержкой идемпотентности, асинхронной очередью задач и реализацией Transactional Outbox Pattern.


## Функционал

- **Создание платежей** — приём платежей с указанием суммы, валюты, описания
- **Идемпотентность** — защита от дублирования через `Idempotency-Key`
- **Асинхронная обработка** — фоновый worker для обработки платежей через RabbitMQ
- **Паттерн Outbox** — надёжная публикация событий через таблицу outbox

---

## Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/VitaliyStrunin/luna
cd luna
```

### 2. Настройка переменных окружения

```bash
cp .env.example .env
```

Отредактируйте `.env` при необходимости (значения по умолчанию работают для локальной разработки).

### 3. Запуск через Docker Compose

```bash
docker-compose up --build
```

Сервисы будут доступны по адресам:

| Сервис | Адрес | Описание |
|--------|-------|----------|
| **API** | http://localhost:8000 | Основной API |
| **PostgreSQL** | localhost:5433 | База данных |
| **RabbitMQ Management** | http://localhost:15672 | Веб-интерфейс RabbitMQ |
| **RabbitMQ** | localhost:5672 | Брокер сообщений |

> **Логин/пароль для RabbitMQ:** `guest` / `guest`

### 4. Service health

```bash
curl http://localhost:8000/health
```

---

## Примеры

### Создание платежа

**POST** `/api/v1/payments`

```bash
curl -X POST http://localhost:8000/api/v1/payments \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: unique-key-123" \
  -H "X-API-Key: some_api_key" \
  -d '{
    "amount": 1000.00,
    "currency": "RUB",
    "description": "Оплата заказа №123",
    "webhook_url": "https://webhook.site/dbd2b505-4652-4136-93f2-9ccfcc84fcdc"
  }'
```

**Ответ (202 Accepted):**

```json
{
  "id": "CREATED ID (UUID format)",
  "status": "pending",
  "created_at": "2026-03-30T12:00:00Z"
}
```

### Получение платежа по ID

**GET** `/api/v1/payments/{payment_id}`

```bash
curl http://localhost:8000/api/v1/payments/ENTER_THE_ID_OF_CREATED_ITEM \
  -H "X-API-Key: some_api_key"
```

**Ответ (200 OK):**

```json
{
  "id": "SOME ID CREATED BEFORE",
  "amount": 1000.00,
  "currency": "RUB",
  "description": "Оплата заказа №123",
  "status": "pending",
  "idempotency_key": "unique-key-123",
  "webhook_url": "https://webhook.site/dbd2b505-4652-4136-93f2-9ccfcc84fcdc",
  "created_at": "2026-03-30T12:00:00Z",
  "processed_at": "2026-03-31T12:00:00Z"
}
```

## Структура проекта

```
luna/
├── backend/
│   ├── src/
│   │   ├── core/                 # Конфигурация, исключения, безопасность
│   │   ├── database/             # Подключение к БД, сессии
│   │   ├── payments/             # Модуль платежей
│   │   │   ├── application/      # Use Cases (бизнес-логика)
│   │   │   ├── domain/           # Сущности, value objects
│   │   │   ├── infrastructure/   # Репозитории, модели БД, брокеры
│   │   │   └── presentation/     # API routes, схемы (schemas)
│   │   └── worker/               # Worker для обработки очереди
│   ├── migrations/               # Alembic миграции
│   ├── main.py                   # Точка входа FastAPI
│   └── alembic.ini               # Конфигурация Alembic
├── docker-compose.yml            # Docker Compose конфигурация
├── Dockerfile.api                # Dockerfile для API
├── Dockerfile.worker             # Dockerfile для Worker
├── pyproject.toml                # Зависимости проекта (uv/pip)
├── pytest.ini                    # Конфигурация pytest
└── .env.example                  # Шаблон переменных окружения
```

### Архитектура модуля платежей 

```
payments/
├── application/      # Слой приложений (Use Cases)
│   └── use_cases/
│       ├── create_payment.py
│       └── get_payment.py
├── domain/           # Доменный слой (бизнес-правила)
│   └── entities/
│       └── payment.py
├── infrastructure/   # Инфраструктурный слой (БД, брокеры)
│   ├── database/
│   │   ├── models/
│   │   ├── repositories/
│   │   └── units/
│   └── messaging/
└── presentation/     # Слой представления (API)
    ├── api/
    └── schemas/
```

---
