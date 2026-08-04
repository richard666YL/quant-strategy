import pandas as pd


def sma(data: pd.Series, window: int) -> pd.Series:
    """
    Simple Moving Average
    """
    return data.rolling(window=window).mean()