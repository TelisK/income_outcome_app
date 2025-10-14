from database import Base
from sqlalchemy import ForeignKey, Column, Float, Date, Integer, String, Boolean, Enum # used to give only two roles for user.


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    active = Column(Boolean, default=True)
    role = Column(Enum('admin', 'user', name='user_roles'), default='user')

class Income(Base):
    __tablename__ = 'income'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True)
    income_cash = Column(Float)
    income_pos = Column(Float)
    income = Column(Float)

class Expenses(Base):
    __tablename__ = 'expenses'
    #id = Column(Integer, primary_key=True, index=True)
    id = Column(Integer, index=True)
    date =  Column(Date, ForeignKey('income.date'), primary_key=True, unique=True)
    expenses = Column(Float)
