import backend
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from starlette.templating import _TemplateResponse

app = FastAPI()
templates = Jinja2Templates("templates")

@app.get("/", response_class=HTMLResponse)
async def root():
    return FileResponse("templates/index.html")

@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, title: str, start_date: str|None=None, end_date: str|None=None):
    request_result = backend.download_news(title, start_date, end_date)
    return process_results(request, request_result, title)

@app.get("/top", response_class=HTMLResponse)
async def top_articles(request: Request):
    request_results = backend.download_top()
    return process_results(request, request_results)

def process_results(request: Request, results: dict, title: str | None = None) -> _TemplateResponse:
    if title is None:
        title = "top articles"
    else:
        title = f'"{title}"'
    if results["status"] == "ok":
        articles = results["articles"]
        return templates.TemplateResponse(
            request=request, name="article_list.j2", context={"article_list": articles, "title": title}
        )
    else:
        return templates.TemplateResponse(
            request=request, name="error.j2", context={"message": results["message"]}
        )
