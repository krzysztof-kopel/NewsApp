from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
import backend

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    return FileResponse("index.html")

@app.get("/search")
async def search(title: str, start_date: str|None=None, end_date: str|None=None):
    return backend.download_news(title, start_date, end_date)
