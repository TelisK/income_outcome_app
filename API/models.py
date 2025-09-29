from database import Base
from sqlalchemy import ForeignKey, Column, Float, Date, Integer

class Income(Base):
    __tablename__ = 'income'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True)
    income_cash = Column(Float)
    income_pos = Column(Float)
    income = Column(Float)

class Expenses(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True, index=True)
    date =  Column(Date, ForeignKey('income.date'), unique=True)
    expenses = Column(Float)
