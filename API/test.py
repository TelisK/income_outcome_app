from fastapi import FastAPI, Path
import sqlite3

app = FastAPI()

@app.get('/')
def index():
    return {'name' : 'first data'}

@app.get('/{date}')
def get_data(date : str):
    conn = sqlite3.connect('../income_outcome.db')
    c = conn.cursor()
    c.execute("SELECT income.date, income.income_cash, income.income_pos, income.income, outcome.outcome FROM income LEFT JOIN outcome ON income.date = outcome.date WHERE income.date = ?", (date,))
    rows = c.fetchall()
    for row in rows:
        if row == date:
            return {'date': rows}
        else:
            return {'data': 'Not Found'}
    conn.close()