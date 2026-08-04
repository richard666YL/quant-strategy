import pandas as pd

from quant_strategy.indicators.moving_average import sma


def generate_ma_cross_signal(
    price: pd.Series,
    short_window: int = 20,
    long_window: int = 50,
) -> pd.DataFrame:
    """Generate moving-average crossover signals."""

    if short_window <= 0 or long_window <= 0:
        raise ValueError("Moving-average windows must be positive.")

    if short_window >= long_window:
        raise ValueError("short_window must be smaller than long_window.")

    result = pd.DataFrame(index=price.index)

    result["price"] = price
    result["short_ma"] = sma(price, short_window)
    result["long_ma"] = sma(price, long_window)

    # 1 = 持有，0 = 空仓
    result["position"] = (
        result["short_ma"] > result["long_ma"]
    ).astype(int)

    # 1 = 买入信号，-1 = 卖出信号，0 = 无交易
    result["signal"] = result["position"].diff().fillna(0)

    return result