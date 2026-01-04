# import requests
# from bs4 import BeautifulSoup
# from datetime import datetime, timedelta
# import time
# import json
# from lxml import html


# HEADERS = {
#     "User-Agent": "Mozilla/5.0"
# }

# MONTH_ID = {
#     "Januari": 1,
#     "Februari": 2,
#     "Maret": 3,
#     "April": 4,
#     "Mei": 5,
#     "Juni": 6,
#     "Juli": 7,
#     "Agustus": 8,
#     "September": 9,
#     "Oktober": 10,
#     "November": 11,
#     "Desember": 12
# }

# START_DATE = datetime(2024, 1, 1)
# END_DATE   = datetime(2025, 12, 31)

# from datetime import datetime, timedelta



# def generate_date_ranges(start_date, end_date, step=2):
#     current = start_date
#     while current <= end_date:
#         yield current, current + timedelta(days=1)
#         current += timedelta(days=step)


# def extract_article_content(soup):
#     """
#     Ambil konten artikel Tempo dengan multi fallback selector
#     """
#     selectors = [
#         {"name": "div", "attrs": {"data-testid": "article-content"}},
#         {"name": "div", "attrs": {"class": "detail__body-text"}},
#         {"name": "div", "attrs": {"itemprop": "articleBody"}},
#         {"name": "div", "attrs": {"class": "article-content"}},
#     ]

#     for sel in selectors:
#         div = soup.find(sel["name"], attrs=sel["attrs"])
#         if div:
#             paragraphs = div.find_all("p")
#             text = " ".join(
#                 p.get_text(strip=True)
#                 for p in paragraphs
#                 if len(p.get_text(strip=True)) > 20
#             )
#             if len(text) > 100:
#                 return text

#     return None


# def parse_tempo_date(raw_date: str) -> datetime:
#     """
#     Contoh input:
#     '30 Desember 2025 | 21.22 WIB'
#     """
#     try:
#         date_part, time_part = raw_date.split("|")
#         date_part = date_part.strip()
#         time_part = time_part.strip().replace("WIB", "").strip()

#         day, month_str, year = date_part.split(" ")
#         hour, minute = time_part.split(".")

#         return datetime(
#             int(year),
#             MONTH_ID[month_str],
#             int(day),
#             int(hour),
#             int(minute)
#         )
#     except Exception as e:
#         raise ValueError(f"Gagal parse tanggal Tempo: {raw_date}") from e


# def extract_tempo_article(url):
#     """Ambil detail artikel (title, published, content)."""
#     r = requests.get(url, headers=HEADERS, timeout=10)
#     if r.status_code != 200:
#         return None
    
#     soup = BeautifulSoup(r.text, "html.parser")

#     script = soup.find("script", type="application/ld+json")
#     if not script:
#         return None
    
#     data = json.loads(script.string)

#     title = data.get("headline")
#     content = data.get("articleBody")
#     published_raw = data.get("datePublished")

#     published = None
#     if published_raw:
#         published = datetime.fromisoformat(
#             published_raw.replace("Z", "+00:00")
#         ).date()
    
#     soup = BeautifulSoup(r.text, "lxml")

#     title_tag = soup.find("h1")
#     if not title_tag:
#         return None
#     title = title_tag.get_text(strip=True)

#     meta_date = soup.find("meta", property="article:published_time")
#     if not meta_date or not meta_date.get("content"):
#         return None
    
#     published = parse_tempo_date(meta_date["content"])

#     content = extract_article_content(soup)
#     if not content:
#         return None

#     return {
#         "title": title,
#         "published_date": published,
#         "content": content,
#         "link": url
#     }

# def crawl_tempo(start_date, end_date, max_pages=50):
    
#     base_url = "https://www.tempo.co/indeks"
#     results = []

#     for page in range(8, max_pages + 1):
#         print(f"[Tempo] Crawling page {page}")

#         params = {
#             "page": page,
#             "category": "date",
#             "start_date": start_date.strftime("%Y-%m-%d"),
#             "end_date": end_date.strftime("%Y-%m-%d")
#         }

#         r = requests.get(base_url, headers=HEADERS, params=params, timeout=10)
#         if r.status_code != 200:
#             break

#         soup = BeautifulSoup(r.text, "lxml")

#         links = soup.select("a[href]")
#         if not links:
#             print("Tidak ada link ditemukan")
#             break

#         page_article_count = 0

#         for a in links:
#             href = a.get("href")

#             if not href:
#                 continue

#             # hanya artikel tempo
#             if not (
#                 "/nasional/" in href
#                 or "/politik/" in href
#                 or "/bisnis/" in href
#             ):
#                 continue

#             if not href.startswith("http"):
#                 url = "https://www.tempo.co" + href
#             else:
#                 url = href

#             detail = extract_tempo_article(url)
#             if not detail:
#                 continue

#             published = detail["published_date"]
#             if not (start_date <= published <= end_date):
#                 continue

#             results.append({
#                 "media": "Tempo.co",
#                 "title": detail["title"],
#                 "published_date": published,
#                 "link": url,
#                 "content": detail["content"],
#                 "sentiment": ""
#             })
#             page_article_count += 1
#             time.sleep(0.5)

#         print(f"  → Artikel valid di page ini: {page_article_count}")

#         if page_article_count == 0:
#             print("Stop: tidak ada artikel valid")
#             break

#     return results

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
