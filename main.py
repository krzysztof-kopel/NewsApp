import backend
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates("templates")

@app.get("/", response_class=HTMLResponse)
async def root():
    return FileResponse("templates/index.html")

@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, title: str, start_date: str|None=None, end_date: str|None=None):
    request_result = backend.download_news(title, start_date, end_date)
    if request_result["status"] == "ok":
        articles = request_result["articles"]
        return templates.TemplateResponse(
            request=request, name="article_list.j2", context={"article_list": articles, "title": title}
        )
    else:
        return templates.TemplateResponse(
            request=request, name="error.j2", context={"message": request_result["message"]}
        )
