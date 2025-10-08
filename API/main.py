from typing import Annotated
from models import Income, Expenses
from pydantic import BaseModel, validator, field_validator
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, Body, HTTPException, UploadFile, File
from database import SessionLocal, Base, engine
from datetime import date
from starlette import status
from PIL import Image
import io
import easyocr
import cv2


app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class IncomeRequest(BaseModel):
    date: date
    income_cash : float
    income_pos : float
    income : float | None = None

    @validator('income', always=True)
    def set_income(cls, v, values):
        if v is None:
            return values.get('income_cash', 0) + values.get('income_pos', 0)
        return v


class IncomeResponse(BaseModel):
    id: int
    date: date
    income_cash: float
    income_pos: float
    income: float

    class Config:
        from_attributes = True

class IncomeUpdateRequest(BaseModel):
    income_cash: float
    income_pos: float
    income: float

    class Config:
        from_attributes = True

class ExpensesRequest(BaseModel):
    date: date
    expenses: float

class ExpensesUpdateRequest(BaseModel):
    expenses: float

@app.get('/', response_model=list[IncomeResponse], status_code=status.HTTP_200_OK)
async def read_all_income(db: db_dependency):
    return db.query(Income).all()

@app.get('/date_reports/{start_date}/{end_date}', status_code=status.HTTP_200_OK)
async def read_date_range_income(db: db_dependency, start_date: date, end_date: date):
    result = db.query(Income).filter(Income.date >= start_date).filter(Income.date <= end_date).all()
    #return result

    start_end_dates = []
    cash_sum_list = []
    pos_sum_list = []
    sum_list = []
    start_end_dates.append(str(result[0].date))
    start_end_dates.append(str(result[-1].date))

    for i in range(len(result)):

        cash_sum_list.append(result[i].income_cash)
        pos_sum_list.append(result[i].income_pos)
        sum_list.append(result[i].income)
        to_return = {
            'Start_Date' : start_end_dates[0],
            'End_Date' : start_end_dates[1],
            'Cash' : sum(cash_sum_list),
            'POS' : sum(pos_sum_list),
            'Sum' : sum(sum_list)
        }

    return to_return, result


@app.post('/income', status_code=status.HTTP_201_CREATED)
async def set_income(db: db_dependency, income_request: IncomeRequest):
    income_model = Income(**income_request.model_dump())
    db.add(income_model)
    db.commit()

'''@app.post('/income/by_image', status_code=status.HTTP_201_CREATED)
async def by_image(db : db_dependency, file : UploadFile = File(...)):
    content = await file.read()
    image = Image.open(io.BytesIO(content))
    
    img = cv2.imread(image.filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    cv2.imread('cleaned.jpg', gray)
    reader = easyocr.Reader(['en'])
    image_output = reader.readtext('cleaned.jpg')
    for (bbox, text, prob) in image_output:
        to_return = {'text': text, 'prob': prob}

    return to_return'''


@app.put('/income/{date}', status_code=status.HTTP_204_NO_CONTENT)
async def update_income(db: db_dependency,
                        income_request: IncomeUpdateRequest,
                        date: date):
    if date is None:
        raise HTTPException(status_code=400, detail='Bad Request')
    income_model = db.query(Income).filter(Income.date == date).first()
    if income_model is None:
        raise HTTPException(status_code=404, detail='Wrong Date')

    income_model.income_cash = income_request.income_cash
    income_model.income_pos = income_request.income_pos
    income_model.income = income_request.income
    db.add(income_model)
    db.commit()

@app.delete('/income/{date}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_income(db: db_dependency, date: date):
    if date is None:
        raise HTTPException(status_code=400, detail='Bad Request')
    income_model = db.query(Income).filter(Income.date == date).first()
    if income_model is None:
        raise HTTPException(status_code=404, detail='Wrong Date')
    db.query(Income).filter(Income.date == date).delete()
    db.commit()

@app.get('/expenses', response_model=list[ExpensesRequest], status_code=status.HTTP_200_OK)
async def read_all_expenses(db: db_dependency):
    return db.query(Expenses).all()

@app.get('/date_reports/expenses/{start_date}/{end_date}', status_code=status.HTTP_200_OK)
async def read_date_range_expenses(db: db_dependency, start_date: date, end_date: date):
    return db.query(Expenses).filter(Expenses.date >= start_date).filter(Expenses.date <= end_date).all()


@app.post('/expenses', status_code=status.HTTP_201_CREATED)
async def set_expenses(db: db_dependency, expenses_request: ExpensesRequest):
    expenses_model = Expenses(**expenses_request.model_dump())
    db.add(expenses_model)
    db.commit()

@app.put('/expenses/{date}', status_code=status.HTTP_204_NO_CONTENT)
async def update_expenses(db: db_dependency, expenses_request: ExpensesUpdateRequest, date: date):
    if date is None:
        raise HTTPException(status_code=400, detail='Bad Request')
    expenses_model = db.query(Expenses).filter(Expenses.date == date).first()
    if expenses_model is None:
        raise HTTPException(status_code=404, detail='Wrong Date')
    expenses_model.expenses = expenses_request.expenses
    db.add(expenses_model)
    db.commit()

@app.delete('/expenses/{date}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_expenses(db: db_dependency, date: date):
    if date is None:
        raise HTTPException(status_code=400, detail='Bad Request')
    expenses_model = db.query(Expenses).filter(Expenses.date == date).first()
    if expenses_model is None:
        raise HTTPException(status_code=404, detail='Wrong Date')
    db.query(Expenses).filter(Expenses.date == date).delete()
    db.commit()