from fastapi import FastAPI
import models
from database import engine
from routers import auth, income_expenses, image_upload

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(income_expenses.router)
app.include_router(image_upload.router)
