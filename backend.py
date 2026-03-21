import httpx

from main import get_config

def download_news(title: str, start_date: str | None = None, end_date: str | None = None, page_size: int | None = None):
    api_key = get_config().NEWS_API_KEY
    page_size = get_config().DEFAULT_PAGE_SIZE if page_size is None else page_size

    print(api_key)

    url = f"https://newsapi.org/v2/everything?q={title}&language=en&pageSize={page_size}"
    if start_date is not None:
        url += f"&from={start_date}"
    if end_date is not None:
        url += f"&to={end_date}"

    headers = {
        "X-Api-Key": api_key
    }
    api_result = httpx.get(url, headers=headers)
    return api_result.json()["articles"]

if __name__ == "__main__":
    print(download_news("Donald Trump"))
