from typing import Annotated
from models import Income
from pydantic import BaseModel, validator, field_validator
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, Body, HTTPException
from database import SessionLocal, Base, engine
from datetime import date
from starlette import status

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

@app.get('/', response_model=list[IncomeResponse], status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Income).all()

@app.post('/income', status_code=status.HTTP_201_CREATED)
async def set_income(db: db_dependency, income_request: IncomeRequest):
    income_model = Income(**income_request.model_dump())
    db.add(income_model)
    db.commit()

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