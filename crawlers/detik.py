import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

from config.keywords import KEYWORDS
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
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
    Ambil isi artikel Detik
    """
    # r = requests.get(url, headers=HEADERS, timeout=20)
    try:
        r = session.get(url, headers=HEADERS, timeout=30)

        if r.status_code != 200:
            print("Failed open:", url)
            return None

        soup = BeautifulSoup(r.text, "html.parser")

        # Title
        title_tag = soup.find("h1", class_="detail__title")
        title = title_tag.get_text(strip=True) if title_tag else ""

        # Date
        date_tag = soup.find("div", class_="detail__date")
        published = ""
        if date_tag:
            # contoh: Selasa, 16 Desember 2025 14:30 WIB
            raw = date_tag.get_text(strip=True)
            published = parse_date_indonesia(raw)

        # Content
        content_div = soup.find("div", class_="detail__body-text")
        if not content_div:
            return None

        paragraphs = content_div.find_all("p")
        content = "\n".join([p.get_text(strip=True) for p in paragraphs])

        full_text = f"{title} {content}".lower()

        if not contains_keyword(full_text):
            return None

        return {
            "title": title,
            "published_date": published,
            "content": content
        }
    except requests.exceptions.ChunkedEncodingError:
        print("⚠️ ChunkedEncodingError, skip article")
        return None

    except requests.exceptions.ReadTimeout:
        print("⚠️ Timeout, skip article")
        return None

    except requests.exceptions.RequestException as e:
        print("⚠️ Request error:", e)
        return None


def parse_date_indonesia(text):
    """
    Selasa, 16 Desember 2025 14:30 WIB
    → 2025-12-16
    """
    try:
        text = text.split(",")[1].strip()
        text = text.replace("WIB", "").strip()

        months = {
            "Jan": "01", "Feb": "02", "Mar": "03",
            "Apr": "04", "Mei": "05", "Jun": "06",
            "Jul": "07", "Agu": "08", "Sep": "09",
            "Okt": "10", "Nov": "11", "Des": "12"
        }

        parts = text.split()
        day = parts[0]
        month = months[parts[1]]
        year = parts[2]

        return f"{year}-{month}-{day.zfill(2)}"
    except:
        return ""


def search_detik_by_keyword(keyword, start_date, end_date):
    """
    Crawl detik search result berdasarkan keyword dan range tanggal
    Format tanggal: DD/MM/YYYY
    """
    all_articles = []
    page = 1

    while True:
        url = (
            "https://www.detik.com/search/searchnews"
            f"?query={keyword}"
            "&siteid=3"
            f"&fromdatex={start_date}"
            f"&todatex={end_date}"
            "&result_type=latest"
            f"&page={page}"
        )

        # print(f"Crawling: {url}")

        # r = requests.get(url, headers=HEADERS, timeout=20)
        r = session.get(url, headers=HEADERS, timeout=30)

        if r.status_code != 200:
            print("Status:", r.status_code)
            break

        soup = BeautifulSoup(r.text, "html.parser")

        items = soup.find_all("article")

        if not items:
            print("No more result pages.")
            break

        for item in items:
            link_tag = item.find("a", href=True)
            if not link_tag:
                continue

            link = link_tag["href"]

            article_data = extract_article_content(link)
            if not article_data:
                continue

            all_articles.append({
                "media": "Detik.com",
                "title": article_data["title"],
                "published_date": article_data["published_date"],
                "link": link,
                "content": article_data["content"],
                "sentiment": ""
            })

            time.sleep(1)

        page += 1
        time.sleep(2)

    return all_articles


def format_date_ddmmyyyy(date_str):
    """
    Input: YYYY-MM-DD
    Output: DD/MM/YYYY
    """
    d = datetime.strptime(date_str, "%Y-%m-%d")
    return d.strftime("%d/%m/%Y")

# # =========================
# # MAIN CRAWLER
# # =========================
def crawl_detik(start_date: str, end_date: str):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    start_date = start_date.strftime("%d/%m/%Y")
    end_date = end_date.strftime("%d/%m/%Y")

    all_data = []
    print("🚀 Mulai crawling Detik...")
    print("Start:", start_date, "End:", end_date)
    for keyword in KEYWORDS:
        # print("\nKeyword:", keyword)
        articles = search_detik_by_keyword(keyword, start_date, end_date)
        all_data.extend(articles)

    return all_data