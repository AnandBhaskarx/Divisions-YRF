import requests
from bs4 import BeautifulSoup

YRF_NEWS_URL = "https://www.yashrajfilms.com/news"

def get_latest_yrf_news(limit=5):
    response = requests.get(YRF_NEWS_URL, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    news_items = []
    links = soup.find_all("a", href=True)

    for link in links:
        href = link["href"]

        if "/news/detail/" in href:
            title = link.get_text(strip=True)
            url = "https://www.yashrajfilms.com" + href

            if title:
                news_items.append((title, url))

        if len(news_items) >= limit:
            break

    return news_items


if __name__ == "__main__":
    print("\n📰 Latest YRF News:\n")

    news = get_latest_yrf_news()

    for i, (title, url) in enumerate(news, 1):
        print(f"{i}. {title}")
        print(f"   {url}\n")
