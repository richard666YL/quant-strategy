from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "data"


def load_daily_data(ticker: str) -> pd.DataFrame:
    """
    Load daily OHLCV data.
    """

    file_path = DATA_DIR / f"{ticker.lower()}_daily.csv"

    if not file_path.exists():
        raise FileNotFoundError(file_path)

    data = pd.read_csv(
        file_path,
        parse_dates=["Date"],
        index_col="Date",
    )

    return data