
# Daily Income & Expense Management

## Description

The application is written in **Python** using **Streamlit** and allows for the entry of daily income (cash & POS) and expenses, as well as the display of aggregated data and statistics through interactive **Altair** charts. All data is stored in a local **SQLite** database (`income_outcome.db`).

## Features

| Tab             | Function         | Description                                                                           |
| --------------- | ---------------- | ------------------------------------------------------------------------------------- |
| Income Entry    | Enter Cash & POS | ➤ Select date ➤ Automatic total calculation ➤ Check/replace existing entry            |
| Expense Entry   | Enter Expenses   | ➤ Select date ➤ Check/replace existing entry                                          |
| View Totals     | Period Report    | ➤ Detailed list of income and expenses ➤ Totals & average                             |
| View Statistics | Charts           | ➤ Filters: Date range / Month / Year ➤ Select income/expenses ➤ Compare across months |

## Technologies

* Python 3.10+
* [Streamlit](https://streamlit.io)
* [pandas](https://pandas.pydata.org)
* [Altair](https://altair-viz.github.io)
* SQLite (Python `sqlite3` module)

## Database Structure

```txt
income_outcome.db
├─ income
│  ├─ date TEXT PRIMARY KEY
│  ├─ income_cash  REAL
│  ├─ income_pos   REAL
│  └─ income       REAL (cash + pos)
└─ outcome
   ├─ date TEXT PRIMARY KEY
   └─ outcome REAL
```

##

### requirements.txt

```
streamlit
pandas
altair
sqlite3
datetime
```

## Run the App

```bash
streamlit run Income_Outcome_App_EN.py
```

The app will automatically launch in your default web browser (e.g., [http://localhost:8501](http://localhost:8501)).

## User Guide

1. **Enter Income**: Select a date → enter cash & POS amounts → click *Submit Income*.
2. **Enter Expenses**: Same process for expense data.
3. **View Totals**: Set a date range → click *Display*.
4. **View Statistics**: Select period & data type → interactive charts will be shown.


