from typing import Annotated

from fastapi import APIRouter, UploadFile, Depends, File
from PIL import Image
import io
import easyocr
import cv2
from starlette import status
from database import SessionLocal
from sqlalchemy.orm import Session
import numpy as np
import re

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


# NEEDS MORE WORK


@router.post('/income/by_image', status_code=status.HTTP_201_CREATED)
async def by_image(db : db_dependency, file : UploadFile = File(...)):
    content = await file.read()
    npimg = np.frombuffer(content, np.uint8)

    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    if img is None:
        return {'error': 'Image is not loaded'}
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    reader = easyocr.Reader(['en'])
    # filter for numbers only
    image_output = reader.readtext(gray, allowlist='0123456789.,')
    corrections = {'O': '0', 'o': '0', 'S': '5', 's': '5', 'l': '1', 'I': '1', 'B': '8'}

    def clean_text(t):
        return ''.join(corrections.get(ch, ch) for ch in t)

    texts = []
    for (bbox, text, prob) in image_output:
        text = clean_text(text)
       # if not re.fullmatch(r'[\d.,]+', text):
       #     continue
        texts.append(text)

    return {"results": texts}
