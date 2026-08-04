import pandas as pd


def run_backtest(
    price: pd.Series,
    position: pd.Series,
    trading_cost: float = 0.001,
) -> pd.DataFrame:
    """
    Run a simple daily backtest.

    trading_cost=0.001 means 0.1% cost for each position change.
    """

    result = pd.DataFrame(index=price.index)

    result["price"] = price
    result["asset_return"] = price.pct_change().fillna(0)

    # 使用前一天的仓位，避免未来函数
    result["position"] = position.shift(1).fillna(0)

    result["turnover"] = result["position"].diff().abs().fillna(0)

    result["trading_cost"] = result["turnover"] * trading_cost

    result["strategy_return"] = (
        result["position"] * result["asset_return"]
        - result["trading_cost"]
    )

    result["buy_hold_equity"] = (
        1 + result["asset_return"]
    ).cumprod()

    result["strategy_equity"] = (
        1 + result["strategy_return"]
    ).cumprod()

    return result