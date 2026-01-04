import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
}

KEYWORDS = [
    "pemerintah",
    "pemerintahan",
    "presiden",
    "wakil presiden",
    "istana",
    "kementerian",
    "menteri",
    "dpr",
    "kebijakan",
    "negara",
    "apbn",
    "kabinet"
]


def parse_datetime(raw_date):
    raw_date = raw_date.replace("WIB", "").strip()
    raw_date = re.sub(r"^[A-Za-z]+,\s*", "", raw_date)

    MONTH_MAP = {
        "Januari": "January",
        "Februari": "February",
        "Maret": "March",
        "April": "April",
        "Mei": "May",
        "Juni": "June",
        "Juli": "July",
        "Agustus": "August",
        "September": "September",
        "Oktober": "October",
        "November": "November",
        "Desember": "December"
    }

    for indo, eng in MONTH_MAP.items():
        raw_date = raw_date.replace(indo, eng)

    formats = [
        "%d %B %Y %H:%M",
        "%d %b %Y %H:%M",
        "%d %B %Y",
        "%d %b %Y"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(raw_date, fmt)
        except ValueError:
            continue

    return None


def get_article_links_by_date(date_str):
    url = f"https://news.detik.com/berita/indeks?date={date_str}"
    r = requests.get(url, headers=HEADERS, timeout=10)
    if r.status_code != 200:
        return []

    soup = BeautifulSoup(r.text, "lxml")
    links = []

    for a in soup.find_all("a", class_="media__link"):
        link = a.get("href")
        title = None

        # 1️⃣ dtr-ttl (jika ada)
        if a.has_attr("dtr-ttl"):
            title = a.get("dtr-ttl")

        # 2️⃣ onclick (_pt(..., "JUDUL", ...))
        if not title and a.has_attr("onclick"):
            onclick = a.get("onclick")
            parts = onclick.split('"')
            if len(parts) >= 6:
                title = parts[3]

        # 3️⃣ fallback dari img alt
        if not title:
            img = a.find("img")
            if img and img.has_attr("alt"):
                title = img.get("alt")

        if title and link:
            links.append((title.strip(), link))

    return links


def extract_article(url):
    r = requests.get(url, headers=HEADERS, timeout=10)
    if r.status_code != 200:
        return None, None

    soup = BeautifulSoup(r.text, "lxml")

    date_tag = soup.find("div", class_="detail__date")
    if not date_tag:
        return None, None

    raw_date = date_tag.get_text(strip=True)
    published = parse_datetime(raw_date)
    if not published:
        return None, None

    paragraphs = soup.find_all("p")
    content = " ".join(p.get_text(strip=True) for p in paragraphs)

    if len(content) < 200:
        return None, None

    return published, content