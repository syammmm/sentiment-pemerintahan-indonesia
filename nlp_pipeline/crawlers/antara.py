import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Still developing
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


def get_article_links_by_date(date_obj):
    """
    Antara pakai format:
    https://www.antaranews.com/indeks/YYYY/MM/DD
    """
    date_str = date_obj.strftime("%Y/%m/%d")
    url = f"https://www.antaranews.com/indeks/{date_str}"

    r = requests.get(url, headers=HEADERS, timeout=10)
    if r.status_code != 200:
        return []

    soup = BeautifulSoup(r.text, "lxml")
    links = []

    for item in soup.find_all("article"):
        a = item.find("a")
        if not a:
            continue

        title = a.get_text(strip=True)
        link = a.get("href")

        if title and link:
            links.append((title, link))

    return links


def extract_article(url):
    r = requests.get(url, headers=HEADERS, timeout=10)
    if r.status_code != 200:
        return None, None

    soup = BeautifulSoup(r.text, "lxml")

    # tanggal
    date_tag = soup.find("span", class_="date")
    if not date_tag:
        return None, None

    raw_date = date_tag.get_text(strip=True)
    try:
        published = datetime.strptime(raw_date, "%d %B %Y %H:%M")
    except:
        return None, None

    # konten
    content_div = soup.find("div", class_="article-content")
    if not content_div:
        return None, None

    paragraphs = content_div.find_all("p")
    content = " ".join(p.get_text(strip=True) for p in paragraphs)

    if len(content) < 200:
        return None, None

    return published, content