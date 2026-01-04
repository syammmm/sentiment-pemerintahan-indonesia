import pandas as pd
from datetime import date, timedelta
from pathlib import Path

from crawlers.detik import get_article_links_by_date,extract_article,KEYWORDS
from crawlers.tempo import crawl_tempo
from config.settings import RAW_DATA_DIR
from config.keywords import KEYWORDS

START_DATE = date(2025, 1, 1)
END_DATE = date(2025, 12, 31)

#DETIK CRAWLER

# results = []
# current = START_DATE

# while current <= END_DATE:
#     date_str = current.strftime("%Y/%m/%d")
#     print(f"Crawling Detik: {date_str}")

#     articles = get_article_links_by_date(date_str)

#     for title, link in articles:
#         published, content = extract_article(link)
#         if not published:
#             continue

#         text = (title + " " + content).lower()
#         if not any(k in text for k in KEYWORDS):
#             continue

#         results.append({
#             "media": "Detik.com",
#             "title": title,
#             "published_date": published.date(),
#             "link": link,
#             "content": content,
#             "sentiment": ""
#         })

#     current += timedelta(days=1)

# df = pd.DataFrame(results)
# df.to_excel(
#     "data/raw/detik_pemerintahan_2024_2025.xlsx",
#     index=False
# )

# print(f"SELESAI — total artikel: {len(df)}")


#TEMPO CRAWLER
if __name__ == "__main__":
    START_DATE = "2025-09-01"
    END_DATE = "2025-09-07"

    print("🚀 Mulai crawling Tempo...")
    data = crawl_tempo(START_DATE, END_DATE)

    df = pd.DataFrame(data)
    df.drop_duplicates(subset=["link"], inplace=True)

    df.to_excel("data/raw/tempo_pemerintahan_2024_2025 1.xlsx", index=False)
    output_path = "data/raw/tempo_pemerintahan_2024_2025..csv"
    df.to_csv(output_path, index=False)

    print(f"✅ Selesai. Total artikel: {len(df)}")
    print(f"📁 File tersimpan: {output_path}")