# Loan Management API

HTTP JSON API сервіс для роботи з кредитною базою даних.

## Технології

- Python 3.9+
- FastAPI
- SQLAlchemy
- MySQL
- PyMySQL

## Запуск

### Варіант 1: Docker Compose (рекомендовано)

Потрібен лише Docker. Одна команда запускає MySQL + API + завантажує тестові дані:

```bash
docker-compose up --build
```

Сервер: http://127.0.0.1:8000

Swagger UI: http://127.0.0.1:8000/docs

Зупинити:

```bash
docker-compose down
```

### Варіант 2: Локальна установка

#### 1. Клонувати репозиторій

```bash
git clone <url>
cd loan-management-api
```

#### 2. Створити віртуальне середовище та встановити залежності

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/Mac
pip install -r requirements.txt
```

#### 3. Налаштувати базу даних MySQL

Створити базу даних `loan_management` та за потреби змінити параметри підключення у файлі `.env`:

```
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/loan_management
```

#### 4. Завантажити тестові дані

```bash
python scripts/load_csv.py
```

Скрипт автоматично створить таблиці та завантажить дані з CSV-файлів (папка `data/`).

#### 5. Запустити сервер

```bash
uvicorn app.main:app --reload
```

Сервер: http://127.0.0.1:8000

Swagger UI: http://127.0.0.1:8000/docs

## Структура БД

- **Users** — клієнти (id, login, registration_date)
- **Credits** — кредити (id, user_id, issuance_date, return_date, actual_return_date, body, percent)
- **Payments** — платежі (id, sum, payment_date, credit_id, type_id)
- **Plans** — плани видач/зборів (id, period, sum, category_id)
- **Dictionary** — довідник категорій (id, name)

## API ендпоінти

### GET /user_credits/{user_id}

Інформація про кредити клієнта.

Для закритих кредитів: дата видачі, дата повернення, сума видачі, відсотки, сума платежів.

Для відкритих кредитів: дата видачі, крайня дата повернення, кількість днів прострочення, сума видачі, відсотки, платежі по тілу та відсоткам.

```
GET http://127.0.0.1:8000/user_credits/1
```

### POST /plans_insert

Завантаження планів з Excel-файлу (.xlsx).

Валідація: перше число місяця, непусті суми, відсутність дублікатів, коректні категорії.

```
POST http://127.0.0.1:8000/plans_insert
Content-Type: multipart/form-data
file: <Excel-файл>
```

Формат Excel: стовпці `period` (дата), `category` (назва категорії), `sum` (сума).

### GET /plans_performance

Виконання планів на певну дату.

```
GET http://127.0.0.1:8000/plans_performance?check_date=2020-06-15
```

### GET /year_performance

Зведена інформація за рік з помісячним групуванням.

```
GET http://127.0.0.1:8000/year_performance?year=2020
```

## Структура проєкту

```
loan-management-api/
├── app/
│   ├── __init__.py
│   ├── main.py          # точка входу FastAPI
│   ├── database.py      # підключення до БД
│   ├── models.py        # SQLAlchemy моделі
│   ├── schemas.py       # Pydantic схеми
│   └── routers/
│       ├── credits.py       # /user_credits
│       ├── plans.py         # /plans_insert, /plans_performance
│       └── performance.py   # /year_performance
├── data/                # CSV-файли з тестовими даними
├── scripts/
│   └── load_csv.py      # скрипт завантаження даних
├── .env                 # параметри підключення до БД
├── requirements.txt
├── Dockerfile           # Docker-образ для API
└── docker-compose.yml   # запуск MySQL + API однією командою
```
