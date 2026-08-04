import pandas as pd

from quant_strategy.indicators.moving_average import sma


def calculate_ma_target_position(
    prices: pd.Series,
    short_window: int = 20,
    long_window: int = 50,
) -> int:
    """Return 1 for holding and 0 for staying in cash."""

    if len(prices) < long_window:
        raise ValueError(
            f"至少需要 {long_window} 个价格，目前只有 {len(prices)} 个。"
        )

    short_ma = sma(prices, short_window).iloc[-1]
    long_ma = sma(prices, long_window).iloc[-1]

    if short_ma > long_ma:
        return 1

    return 0