from httpx import Response

from config import get_config

async def download_news(title: str, start_date: str | None = None, end_date: str | None = None, page_size: int | None = None) -> dict:
    api_key = get_config().NEWS_API_KEY
    page_size = get_config().DEFAULT_PAGE_SIZE if page_size is None else page_size
    client = get_config().ASYNC_CLIENT

    url = f"https://newsapi.org/v2/everything?q={title}&language=en&pageSize={page_size}"
    if start_date is not None:
        url += f"&from={start_date}"
    if end_date is not None:
        url += f"&to={end_date}"

    headers = {
        "X-Api-Key": api_key
    }

    api_result = await client.get(url, headers=headers)

    return process_articles(api_result)

async def download_top(page_size: int | None = None) -> dict:
    api_key = get_config().NEWS_API_KEY
    page_size = get_config().DEFAULT_PAGE_SIZE if page_size is None else page_size
    client = get_config().ASYNC_CLIENT

    url = f"https://newsapi.org/v2/top-headlines?pageSize={page_size}&language=en"
    headers = {
        "X-Api-Key": api_key
    }

    api_result = await client.get(url, headers=headers)

    return process_articles(api_result)

async def translate(text: str) -> str:
    api_key = get_config().DEEPL_API_KEY
    client = get_config().ASYNC_CLIENT

    url = "https://api-free.deepl.com/v2/translate"
    headers = {
        "Authorization": f"DeepL-Auth-Key {api_key}",
        "Content-type": "application/json"
    }

    request = {
        "text": [text],
        "target_lang": "PL"
    }

    api_results = await client.post(url, headers=headers, json=request)
    api_results = api_results.json()
    return api_results["translations"][0]["text"]

def process_articles(api_result: Response) -> dict:
    data = api_result.json()
    if "articles" in data:
        articles = data["articles"]
        # Deleting time from datetime
        for i in range(len(articles)):
            articles[i]["publishedAt"] = articles[i]["publishedAt"][:10]

        return {"status": "ok", "articles": articles}
    return data
