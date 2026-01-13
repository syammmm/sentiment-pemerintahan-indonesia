import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

RSS_URL = "https://rss.kompas.com/politik"


def parse_date(date_struct):
    try:
        return datetime(*date_struct[:6])
    except:
        return None


def extract_content_and_date(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "lxml")

        # tanggal
        date_tag = soup.find("div", class_="read__time")
        if not date_tag:
            return None, None

        date_text = date_tag.get_text(strip=True)
        date_text = date_text.replace("WIB", "").strip()
        published = datetime.strptime(date_text, "%d/%m/%Y, %H:%M")

        # konten
        article = soup.find("div", class_="read__content")
        if not article:
            return None, None

        paragraphs = article.find_all("p")
        content = " ".join(p.get_text(strip=True) for p in paragraphs)

        return published, content
    except:
        return None, None


def crawl_kompas(start_date, end_date, keywords):
    feed = feedparser.parse(RSS_URL)
    results = []

    for entry in feed.entries:
        try:
            published = parse_date(entry.published_parsed)
            if not published:
                continue

            if not (start_date <= published <= end_date):
                continue

            title = entry.title
            link = entry.link

            published_detail, content = extract_content_and_date(link)
            if not content or not published_detail:
                continue

            combined = f"{title} {content}".lower()
            matched = [k for k in keywords if k.lower() in combined]

            if not matched:
                continue

            results.append({
                "media": "Kompas.com",
                "title": title,
                "published_date": published_detail.date(),
                "link": link,
                "content": content,
                "keyword_match": ", ".join(matched),
                "sentiment": ""
            })

        except:
            continue

    return results