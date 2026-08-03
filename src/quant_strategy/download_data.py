from pathlib import Path

import yfinance as yf


DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

print("Downloading QQQ...")

data = yf.download(
    "QQQ",
    start="2010-01-01",
    auto_adjust=False,
    progress=False,
    multi_level_index=False,
)

csv_file = DATA_DIR / "qqq_daily.csv"

data.to_csv(csv_file)

print(f"Downloaded {len(data)} rows.")
print(f"Saved to: {csv_file}")
print()
print(data.head())