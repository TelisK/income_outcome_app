# Daily Income & Expense Management (+ API)

## Description

The application is written in Python using Streamlit and allows for the entry of daily income (cash & POS) and expenses, as well as the display of aggregated data and statistics through interactive Altair charts.  
All data is stored in a local SQLite database (`income_outcome.db`).

In addition to the Streamlit app, the project now includes a separate API module built with FastAPI.  
The API provides authentication, user management, and endpoints for income and expense data.

## Project Presentation
This project was developed as part of a university course.  
Watch the official presentation video on the professor’s YouTube channel (Greek Language):
https://www.youtube.com/watch?v=_u3T-ewSns0&t=5s

---

## Features

| Tab | Function | Description |
|------|-----------|-------------|
| Income Entry | Enter Cash & POS | Select date, automatic total calculation, check/replace existing entry |
| Expense Entry | Enter Expenses | Select date, check/replace existing entry |
| View Totals | Period Report | Detailed list of income and expenses, totals and averages |
| View Statistics | Charts | Filters: date range, month, year; select income/expenses; compare across months |

---

## Technologies

- Python 3.10+
- Streamlit
- FastAPI
- pandas
- Altair
- SQLite (sqlite3)
- SQLAlchemy
- python-jose
- passlib (bcrypt)
- uvicorn

---

## Database Structure

```

income_outcome.db
├─ income
│  ├─ id INTEGER PRIMARY KEY
│  ├─ date DATE UNIQUE
│  ├─ income_cash REAL
│  ├─ income_pos REAL
│  └─ income REAL (cash + pos)
├─ expenses
│  ├─ id INTEGER
│  ├─ date DATE PRIMARY KEY (FK → income.date)
│  └─ expenses REAL
└─ users
├─ id INTEGER PRIMARY KEY
├─ username TEXT UNIQUE
├─ email TEXT
├─ first_name TEXT
├─ last_name TEXT
├─ hashed_password TEXT
├─ role TEXT (admin or user)
└─ active BOOLEAN

```

---

## Folder Structure

```

.
├── Income_Outcome_App_EN.py        # Streamlit app
├── requirements.txt
├── income_outcome.db
└── API/
├── main.py                     # FastAPI entry point
├── models.py                   # Database models
├── database.py                 # DB configuration
└── routers/
├── auth.py                 # Authentication (JWT, roles)
├── income_expenses.py      # Income & expenses endpoints
└── image_upload.py         # Optional image upload

```

---

## Requirements

```

streamlit
pandas
altair
sqlite3
datetime
fastapi
uvicorn
sqlalchemy
python-jose
passlib[bcrypt]

```

---

## Streamlit Application

### Run the App

```

streamlit run Income_Outcome_App_EN.py

```

The app will automatically launch in your default web browser, usually at  
http://localhost:8501

### User Guide

1. Enter Income: Select a date, enter cash & POS amounts, click "Submit Income".  
2. Enter Expenses: Same process for expense data.  
3. View Totals: Set a date range and click "Display".  
4. View Statistics: Select period & data type to display interactive charts.

---

## API Module (FastAPI Backend)

The `API/` folder contains a standalone FastAPI backend that provides authentication and RESTful access to the income and expense data.  
It supports JWT authentication, role-based access control (`admin`, `user`), and date range reporting.

### Run the API

```

cd API
uvicorn main:app --reload

````

The API will be available at  
http://localhost:8000

Swagger documentation:  
http://localhost:8000/docs  
ReDoc documentation:  
http://localhost:8000/redoc

---

### API Overview

#### Authentication Endpoints

| Method | Endpoint | Description |
|---------|-----------|-------------|
| POST | `/auth/` | Create a new user |
| POST | `/auth/token` | Obtain JWT access token |

Example - Create User:
```json
{
  "username": "admin",
  "email": "admin@example.com",
  "first_name": "Admin",
  "last_name": "User",
  "password": "1234",
  "role": "admin"
}
````

---

#### Income Endpoints

| Method | Endpoint                                | Description                         |
| ------ | --------------------------------------- | ----------------------------------- |
| GET    | `/`                                     | Get all income records (admin only) |
| POST   | `/income`                               | Add a new income record             |
| PUT    | `/income/{date}`                        | Update an existing income record    |
| DELETE | `/income/{date}`                        | Delete an income record             |
| GET    | `/date_reports/{start_date}/{end_date}` | Get income summary for a date range |

---

#### Expenses Endpoints

| Method | Endpoint                                         | Description                          |
| ------ | ------------------------------------------------ | ------------------------------------ |
| GET    | `/expenses`                                      | Get all expense records              |
| POST   | `/expenses`                                      | Add a new expense record             |
| PUT    | `/expenses/{date}`                               | Update an existing expense record    |
| DELETE | `/expenses/{date}`                               | Delete an expense record             |
| GET    | `/date_reports/expenses/{start_date}/{end_date}` | Get expense summary for a date range |

---

### Example Workflow

```
# Login to obtain a token
POST http://localhost:8000/auth/token
Content-Type: application/x-www-form-urlencoded

username=admin&password=1234
```

```
# Add an income entry
POST http://localhost:8000/income
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

{
  "date": "2025-10-05",
  "income_cash": 100.0,
  "income_pos": 50.0
}
```

---

## License

This project is licensed under the MIT License.
