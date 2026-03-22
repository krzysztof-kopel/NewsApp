import httpx
from httpx import Response

from config import get_config

def download_news(title: str, start_date: str | None = None, end_date: str | None = None, page_size: int | None = None) -> dict:
    api_key = get_config().NEWS_API_KEY
    page_size = get_config().DEFAULT_PAGE_SIZE if page_size is None else page_size

    url = f"https://newsapi.org/v2/everything?q={title}&language=en&pageSize={page_size}"
    if start_date is not None:
        url += f"&from={start_date}"
    if end_date is not None:
        url += f"&to={end_date}"

    headers = {
        "X-Api-Key": api_key
    }
    api_result = httpx.get(url, headers=headers)

    return process_articles(api_result)

def download_top(page_size: int | None = None) -> dict:
    api_key = get_config().NEWS_API_KEY
    page_size = get_config().DEFAULT_PAGE_SIZE if page_size is None else page_size

    url = f"https://newsapi.org/v2/top-headlines?pageSize={page_size}&language=en"
    headers = {
        "X-Api-Key": api_key
    }
    api_result = httpx.get(url, headers=headers)

    return process_articles(api_result)

def translate(title: str, description: str) -> dict[str, str]:
    api_key = get_config().DEEPL_API_KEY

    url = "https://api-free.deepl.com/v2/translate"
    headers = {
        "Authorization": f"DeepL-Auth-Key {api_key}",
        "Content-type": "application/json"
    }

    request = {
        "text": [title, description],
        "target_lang": "PL"
    }

    api_results = httpx.post(url, headers=headers, json=request)
    api_results = api_results.json()
    return {"title": api_results["translations"][0]["text"], "description": api_results["translations"][1]["text"]}

def process_articles(api_result: Response) -> dict:
    if "articles" in api_result.json():
        articles = api_result.json()["articles"]
        # Deleting time from datetime
        for i in range(len(articles)):
            articles[i]["publishedAt"] = articles[i]["publishedAt"][:10]

        return {"status": "ok", "articles": articles}
    return api_result.json()

if __name__ == "__main__":
    print(download_news("Donald Trump"))
    print(translate("A simple title", "A simple description"))
