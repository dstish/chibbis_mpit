from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
from typing import Optional
from review_analysis import analyze_reviews  # Импортируем функцию из review_analysis.py

app = FastAPI(title="Revi AI", description="Сервис анализа отзывов о доставке еды", version="1.0")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Revi AI</title>
    </head>
    <body>
        <h1>Загрузите Excel файл с отзывами</h1>
        <form action="/uploadfile/" enctype="multipart/form-data" method="post">
            <input name="file" type="file">
            <button type="submit">Let's Go</button>
        </form>
    </body>
    </html>
    """

@app.post("/uploadfile/")
def upload_file(file: UploadFile):
    if not file.filename.endswith('.xlsx'):
        raise HTTPException(status_code=400, detail="Только Excel файлы поддерживаются")
    
    df = pd.read_excel(file.file)
    if 'Review' not in df.columns:
        raise HTTPException(status_code=400, detail="Отсутствует колонка 'Review' в файле")

    # Используем функцию из review_analysis для анализа отзывов
    results = analyze_reviews(df)

    return {"results": results}

