import requests
import time
import json
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import List, Dict
import random
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# =========================
# DATE RANGE GENERATOR
# =========================
def generate_date_ranges(start_date: datetime, end_date: datetime):
    current = start_date
    while current <= end_date:
        yield current, current + timedelta(days=1)
        current += timedelta(days=2)

# =========================
# GET ARTICLE LINKS
# =========================
def safe_get(url, session, retries=5):
    for i in range(retries):
        r = session.get(url, timeout=20)
        if r.status_code == 200:
            return r

        if r.status_code == 429:
            wait = 5 * (i + 1)
            print(f"⚠️ 429 detected, retry in {wait}s")
            time.sleep(wait)

        else:
            return None

    return None

def get_article_links(start_date: datetime, end_date: datetime, page: int) -> List[str]:
    url = (
        "https://www.tempo.co/indeks?"
        f"page={page}&category=date"
        f"&start_date={start_date.strftime('%Y-%m-%d')}"
        f"&end_date={end_date.strftime('%Y-%m-%d')}"
    )

    #r = requests.get(url, headers=HEADERS, timeout=15)
    session = requests.Session()
    session.headers.update(HEADERS)
    r = safe_get(url, session)
    if not r:
        return []

    soup = BeautifulSoup(r.text, "lxml")

    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if not href.startswith("http"):
            url = "https://www.tempo.co" + href
        else:
            url = href
        if (
                 "/nasional/" in href
                 or "/politik/" in href
                 or "/bisnis/" in href
             ):
            links.append(url)

    return list(set(links))

# =========================
# EXTRACT ARTICLE CONTENT
# =========================
def extract_article(url: str) -> Dict | None:
    
    # r = requests.get(url, headers=HEADERS, timeout=15)
    # if r.status_code != 200:
    #     return None
    
    session = requests.Session()
    session.headers.update(HEADERS)
    r = safe_get(url, session)
    if not r:
        return []

    soup = BeautifulSoup(r.text, "lxml")

    script = soup.find("script", type="application/ld+json")
    if not script:
        return None

    try:
        data = json.loads(script.string)
    except Exception:
        return None

    title = data.get("headline")
    content = data.get("articleBody")
    published_raw = data.get("datePublished")

    if not title or not content or not published_raw:
        return None

    published = datetime.fromisoformat(
        published_raw.replace("Z", "+00:00")
    ).date()

    return {
        "media": "Tempo",
        "title": title.strip(),
        "published_date": published.strftime("%Y-%m-%d"),
        "link": url,
        "content": content.strip(),
        "sentiment": ""
    }

# =========================
# MAIN CRAWLER
# =========================
def crawl_tempo(start_date: str, end_date: str, max_pages: int = 50) -> List[Dict]:
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    results = []
    print("🚀 Mulai crawling Tempo...")
    for range_start, range_end in generate_date_ranges(start, end):
        print(f"[DATE] {range_start.date()} → {range_end.date()}")

        for page in range(1, max_pages + 1):
            links = get_article_links(range_start, range_end, page)

            if not links:
                break

            for link in links:
                article = extract_article(link)
                if article:
                    results.append(article)

            time.sleep(random.uniform(3, 8))  # anti-block

    return results
