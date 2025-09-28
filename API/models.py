from database import Base
from sqlalchemy import Column, Float, Date, Integer

class Income(Base):
    __tablename__ = 'income'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True)
    income_cash = Column(Float)
    income_pos = Column(Float)
    income = Column(Float)