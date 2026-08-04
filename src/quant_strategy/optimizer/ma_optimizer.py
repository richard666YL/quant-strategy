from itertools import product

import pandas as pd

from quant_strategy.backtest.simple_backtest import run_backtest
from quant_strategy.performance.metrics import (
    calculate_cagr,
    calculate_max_drawdown,
    calculate_sharpe_ratio,
)
from quant_strategy.signals.ma_cross_signal import generate_ma_cross_signal


def optimize_ma_parameters(
    price: pd.Series,
    short_windows: list[int],
    long_windows: list[int],
    trading_cost: float = 0.001,
) -> pd.DataFrame:
    """
    Test multiple short/long moving-average combinations.

    Returns one row for every valid parameter combination.
    """

    optimization_results: list[dict[str, float | int]] = []

    for short_window, long_window in product(
        short_windows,
        long_windows,
    ):
        if short_window >= long_window:
            continue

        signals = generate_ma_cross_signal(
            price=price,
            short_window=short_window,
            long_window=long_window,
        )

        backtest_result = run_backtest(
            price=price,
            position=signals["position"],
            trading_cost=trading_cost,
        )

        strategy_equity = backtest_result["strategy_equity"]
        strategy_returns = backtest_result["strategy_return"]

        trade_count = int(signals["signal"].abs().sum())

        optimization_results.append(
            {
                "short_window": short_window,
                "long_window": long_window,
                "final_equity": strategy_equity.iloc[-1],
                "cagr": calculate_cagr(strategy_equity),
                "max_drawdown": calculate_max_drawdown(
                    strategy_equity
                ),
                "sharpe_ratio": calculate_sharpe_ratio(
                    strategy_returns
                ),
                "trade_count": trade_count,
            }
        )

    results = pd.DataFrame(optimization_results)

    if results.empty:
        raise ValueError(
            "No valid parameter combinations were tested."
        )

    return results