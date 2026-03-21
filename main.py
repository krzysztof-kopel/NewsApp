from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def root():
    return FileResponse("index.html")
