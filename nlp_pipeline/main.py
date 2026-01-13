import pandas as pd
from datetime import date

from crawlers.detik import crawl_detik
from crawlers.tempo import crawl_tempo
from crawlers.cnn import crawl_cnn
from config.settings import RAW_DATA_DIR, create_timestamp

START_DATE = date(2025, 7, 1)
END_DATE = date(2025, 7, 31)

# Name output file
excel_path = RAW_DATA_DIR / "media_elektronik_2025_Juli.xlsx"
csv_path = RAW_DATA_DIR / "media_elektronik_2025_Juli.csv"
#MAIN CRAWLER
if __name__ == "__main__":
    START_DATE = START_DATE.strftime("%Y-%m-%d")
    END_DATE = END_DATE.strftime("%Y-%m-%d")

    print("Start Time :", create_timestamp())
    data_tempo = crawl_tempo(START_DATE, END_DATE)
    print("Finish Time Tempo:", create_timestamp())
    data_detik = crawl_detik(START_DATE, END_DATE)
    print("Finish Time Detik:", create_timestamp())
    data_cnn = crawl_cnn(START_DATE, END_DATE)
    print("Finish Time CNN:", create_timestamp())
    data_all = data_cnn + data_tempo + data_detik
    print("Finish Time ALL:", create_timestamp())

    df = pd.DataFrame(data_all)
    df.drop_duplicates(subset=["link"], inplace=True)
    print(f"✅ Total artikel Tempo: {len(data_tempo)}")
    print(f"✅ Total artikel Detik: {len(data_detik)}")
    print(f"✅ Total artikel CNN: {len(data_cnn)}")
    print(f"✅ Total artikel: {len(df)}")

    # Save to Excel & CSV

    # Simpan file
    df.to_excel(excel_path, index=False)
    df.to_csv(csv_path, index=False)

    print(f"📁 File tersimpan: {RAW_DATA_DIR}")