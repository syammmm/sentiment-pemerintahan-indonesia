import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
from config.keywords import KEYWORDS
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

def create_session():
    session = requests.Session()

    retries = Retry(
        total=5,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )

    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    return session


session = create_session()

def contains_keyword(text):
    text = text.lower()
    return any(k in text for k in KEYWORDS)


def extract_article_content(url):
    """
    Ambil isi artikel CNN Indonesia
    """
    # r = requests.get(url, headers=HEADERS, timeout=20)
    try:
        r = session.get(url, headers=HEADERS, timeout=30)


        if r.status_code != 200:
            print("Failed open:", url)
            return None

        soup = BeautifulSoup(r.text, "html.parser")
        if not soup:
            print("Skip page karena error")
            page += 1
            time.sleep(5)
            return None

        # Title
        title_tag = soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else ""

        # Date
        date_tag = soup.find("meta", {"name": "dtk:publishdate"})
        published = ""
        if date_tag:
            published_raw = date_tag.get("content")  # 2025/12/01 23:30:21'
            published = published_raw.split(" ")[0]
            published = datetime.strptime(published, "%Y/%m/%d").date()
            published = published.strftime("%Y-%m-%d")

        # Content
        content_div = soup.find("div", class_="detail-text")
        if not content_div:
            return None

        paragraphs = content_div.find_all("p")
        content = "\n".join([p.get_text(strip=True) for p in paragraphs])

        # Filter keyword
        full_text = f"{title} {content}".lower()

        if not contains_keyword(full_text):
            return None

        return {
            "title": title,
            "published_date": published,
            "content": content
        }
    except requests.exceptions.ChunkedEncodingError:
        print("ChunkedEncodingError, skip article")
        return None

    except requests.exceptions.ReadTimeout:
        print("Timeout, skip article")
        return None

    except requests.exceptions.RequestException as e:
        print("Request error:", e)
        return None


def get_articles_by_date(date_str):
    """
    Crawl semua artikel CNN nasional indeks/3 per tanggal
    """
    all_articles = []
    page = 1

    while True:
        url = f"https://www.cnnindonesia.com/nasional/indeks/3?date={date_str}&page={page}"
        # print(f"Crawling: {url}")

        # r = requests.get(url, headers=HEADERS, timeout=20)
        r = session.get(url, headers=HEADERS, timeout=30)

        if r.status_code != 200:
            print("Status:", r.status_code)
            break

        soup = BeautifulSoup(r.text, "html.parser")
        if not soup:
            print("Skip page karena error")
            page += 1
            time.sleep(5)
            continue

        articles = soup.find_all("article")

        if not articles:
            print("No articles found, stop pagination.")
            break

        for art in articles:
            link_tag = art.find("a", href=True)
            if not link_tag:
                continue

            link = link_tag["href"]

            article_data = extract_article_content(link)
            if not article_data:
                continue

            all_articles.append({
                "media": "CNNIndonesia",
                "title": article_data["title"],
                "published_date": article_data["published_date"],
                "link": link,
                "content": article_data["content"],
                "sentiment": ""
            })

            time.sleep(1)  # delay antar artikel

        page += 1
        time.sleep(3)  # delay antar halaman

    return all_articles


def generate_date_range(start_date, end_date):
    """
    Format input: YYYY-MM-DD
    Output: YYYY/MM/DD
    """
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    dates = []
    while start <= end:
        dates.append(start.strftime("%Y/%m/%d"))
        start += timedelta(days=1)

    return dates

# =========================
# MAIN CRAWLER
# =========================
def crawl_cnn(start_date: str, end_date: str):
    all_data = []

    dates = generate_date_range(start_date, end_date)
    print("🚀 Mulai crawling CNN...")
    for d in dates:
        print("\nTanggal:", d)
        articles = get_articles_by_date(d)
        if not articles:
            time.sleep(2)
            continue
        all_data.extend(articles)
        time.sleep(2)
    return all_data