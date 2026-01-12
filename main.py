import pandas as pd
from datetime import date, timedelta


from crawlers.detik import crawl_detik
from crawlers.tempo import crawl_tempo
from crawlers.cnn import crawl_cnn
from config.settings import RAW_DATA_DIR
from config.keywords import KEYWORDS

START_DATE = date(2025, 4, 1)
END_DATE = date(2025, 4, 30)

#MAIN CRAWLER
if __name__ == "__main__":
    START_DATE = START_DATE.strftime("%Y-%m-%d")
    END_DATE = END_DATE.strftime("%Y-%m-%d")

    data_tempo = crawl_tempo(START_DATE, END_DATE)
    data_detik = crawl_detik(START_DATE, END_DATE)
    data_cnn = crawl_cnn(START_DATE, END_DATE)
    data_all = data_cnn + data_tempo + data_detik

    df = pd.DataFrame(data_all)
    df.drop_duplicates(subset=["link"], inplace=True)
    print(f"✅ Total artikel Tempo: {len(data_tempo)}")
    print(f"✅ Total artikel Detik: {len(data_detik)}")
    print(f"✅ Total artikel CNN: {len(data_cnn)}")
    print(f"✅ Total artikel: {len(df)}")
    df.to_excel("data/raw/media_elektronik_2024_2025_April.xlsx", index=False)
    output_path = "data/raw/media_elektronik_2024_2025_April.csv"
    df.to_csv(output_path, index=False)

    print(f"📁 File tersimpan: {output_path}")