# Loan Management API

HTTP JSON API service for managing a loan database.

## Tech Stack

- Python 3.9+
- FastAPI
- SQLAlchemy
- MySQL
- PyMySQL

## Getting Started

### Option 1: Docker Compose (recommended)

Requires only Docker. A single command starts MySQL + API and loads test data:

```bash
docker-compose up --build
```

Server: http://127.0.0.1:8000

Swagger UI: http://127.0.0.1:8000/docs

Stop:

```bash
docker-compose down
```

### Option 2: Local Setup

#### 1. Clone the repository

```bash
git clone <https://github.com/VladyslavOliinyk/loan-management-api.git>
cd loan-management-api
```

#### 2. Create a virtual environment and install dependencies

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/Mac
pip install -r requirements.txt
```

#### 3. Configure MySQL database

Create the `loan_management` database and update connection settings in `.env` if needed:

```bash
cp .env.example .env
```

```
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/loan_management
```

#### 4. Load test data

```bash
python scripts/load_csv.py
```

The script automatically creates tables and loads data from CSV files (`data/` folder).

#### 5. Start the server

```bash
uvicorn app.main:app --reload
```

Server: http://127.0.0.1:8000

Swagger UI: http://127.0.0.1:8000/docs

## Database Schema

- **Users** — clients (id, login, registration_date)
- **Credits** — issued loans (id, user_id, issuance_date, return_date, actual_return_date, body, percent)
- **Payments** — loan payments (id, sum, payment_date, credit_id, type_id)
- **Plans** — monthly issuance/collection plans (id, period, sum, category_id)
- **Dictionary** — category reference (id, name)

## API Endpoints

### GET /user_credits/{user_id}

Returns credit information for a specific user.

Closed credits: issuance date, return date, loan body, interest, total payments.

Open credits: issuance date, due date, overdue days, loan body, interest, body payments, interest payments.

```
GET http://127.0.0.1:8000/user_credits/1
```

### POST /plans_insert

Upload monthly plans from an Excel file (.xlsx).

Validation: period must be the first day of the month, sums must not be empty, no duplicates allowed, categories must exist.

```
POST http://127.0.0.1:8000/plans_insert
Content-Type: multipart/form-data
file: <Excel file>
```

Excel format: columns `period` (date), `category` (category name), `sum` (amount).

### GET /plans_performance

Plan performance as of a given date.

```
GET http://127.0.0.1:8000/plans_performance?check_date=2020-06-15
```

### GET /year_performance

Yearly summary with monthly breakdown.

```
GET http://127.0.0.1:8000/year_performance?year=2020
```

## Project Structure

```
loan-management-api/
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI entry point
│   ├── database.py        # database connection
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic schemas
│   └── routers/
│       ├── credits.py         # /user_credits
│       ├── plans.py           # /plans_insert, /plans_performance
│       └── performance.py     # /year_performance
├── data/                  # CSV test data
├── scripts/
│   └── load_csv.py        # data loading script
├── .env.example           # environment variables template
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```
