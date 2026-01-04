import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import locale

# Set locale Indonesia (Mac)
try:
    locale.setlocale(locale.LC_TIME, "id_ID.UTF-8")
except:
    pass

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

BASE_SEARCH_URL = "https://www.cnnindonesia.com/search/?query={keyword}&page={page}"


def parse_date(date_text):
    """
    Contoh:
    'Selasa, 2 Januari 2024 14:30 WIB'
    """
    try:
        date_text = date_text.replace("WIB", "").strip()
        return datetime.strptime(date_text, "%A, %d %B %Y %H:%M")
    except:
        return None


def extract_content(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "lxml")

        content_div = soup.find("div", class_="detail-text")
        if not content_div:
            return None

        paragraphs = content_div.find_all("p")
        text = " ".join(p.get_text(strip=True) for p in paragraphs)

        return text if len(text) > 300 else None
    except:
        return None


def crawl_cnn(start_date, end_date, keywords, max_pages=10):
    results = []

    for keyword in keywords:
        print(f"\n🔍 Keyword: {keyword}")

        for page in range(1, max_pages + 1):
            url = BASE_SEARCH_URL.format(keyword=keyword, page=page)
            print(f"  → Page {page}")

            r = requests.get(url, headers=HEADERS)
            if r.status_code != 200:
                break

            soup = BeautifulSoup(r.text, "lxml")

            container = soup.find("div", class_="list media_rows")
            if not container:
                print("    ❌ Container kosong")
                break

            articles = container.find_all("article")
            if not articles:
                print("    ❌ Tidak ada article")
                break

            for art in articles:
                try:
                    a_tag = art.find("a")
                    date_tag = art.find("span", class_="date")

                    if not a_tag or not date_tag:
                        continue

                    title = a_tag.get_text(strip=True)
                    link = a_tag["href"]
                    published = parse_date(date_tag.get_text(strip=True))

                    if not published:
                        continue

                    if not (start_date <= published <= end_date):
                        continue

                    content = extract_content(link)
                    if not content:
                        continue

                    results.append({
                        "media": "CNN Indonesia",
                        "title": title,
                        "published_date": published.date(),
                        "link": link,
                        "content": content,
                        "keyword_match": keyword,
                        "sentiment": ""
                    })

                except Exception as e:
                    continue

            time.sleep(1)

    return results