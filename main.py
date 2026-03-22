from fastapi.params import Form

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

@app.get("img/icon.svg", response_class=FileResponse)
def icon():
    return FileResponse("img/icon.svg", media_type="image/svg+xml")

@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, title: str, start_date: str|None=None, end_date: str|None=None, page_size: int|None = None):
    if page_size is not None and page_size > 10:
        return handle_error(request, "You can't request that many articles.")
    elif start_date is not None and end_date is not None and start_date > end_date:
        return handle_error(request, "Start date must happen earlier than end date.")
    request_result = backend.download_news(title, start_date, end_date, page_size)
    return process_results(request, request_result, title)

@app.get("/top", response_class=HTMLResponse)
async def top_articles(request: Request):
    request_results = backend.download_top()
    return process_results(request, request_results)

@app.post("/translate", response_class=HTMLResponse)
async def translate(request: Request, source_name: str=Form(), publishedAt: str=Form(), title: str=Form(),
                    author: str=Form(), urlToImage: str=Form(), description: str=Form(), url: str=Form()):
    translation = backend.translate(title, description)
    return templates.TemplateResponse(
        request=request, name="translation.j2", context={
            "article": {"source": {"name": source_name}, "publishedAt": publishedAt, "title": translation["title"],
                              "author": author, "urlToImage": urlToImage, "description": translation["description"],
                              "url": url}
        }
    )

def handle_error(request: Request, message: str) -> _TemplateResponse:
    return templates.TemplateResponse(
        request=request, name="error.j2", context={
            "message": message
        }
    )

def process_results(request: Request, results: dict, title: str | None = None, translate: bool = True) -> _TemplateResponse:
    if title is None:
        title = "top articles"
    else:
        title = f'"{title}"'
    if results["status"] == "ok":
        articles = results["articles"]
        if len(articles) >= 1:
            return templates.TemplateResponse(
                request=request, name="article_list.j2", context={"article_list": articles,
                                                                  "number_of_articles": len(articles),
                                                                  "title": title, "translate": translate}
            )
        else:
            return templates.TemplateResponse(
                request=request, name="article_list.j2", context={"title": title}
            )
    else:
        return templates.TemplateResponse(
            request=request, name="error.j2", context={"message": results["message"]}
        )
