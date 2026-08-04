import pandas as pd

from quant_strategy.performance.metrics import (
    calculate_annual_volatility,
    calculate_cagr,
    calculate_max_drawdown,
    calculate_sharpe_ratio,
)


def print_performance_report(
    result: pd.DataFrame,
    strategy_name: str,
) -> None:
    """Print a performance comparison report."""

    strategy_equity = result["strategy_equity"]
    buy_hold_equity = result["buy_hold_equity"]

    strategy_returns = result["strategy_return"]
    buy_hold_returns = result["asset_return"]

    print("=" * 45)
    print("Strategy Performance Report")
    print("=" * 45)

    print(f"Strategy: {strategy_name}")
    print(
        f"Period: {result.index.min().date()} "
        f"to {result.index.max().date()}"
    )
    print()

    print("=== Strategy ===")
    print(f"Final equity: {strategy_equity.iloc[-1]:.2f}")
    print(f"CAGR: {calculate_cagr(strategy_equity):.2%}")
    print(
        f"Maximum drawdown: "
        f"{calculate_max_drawdown(strategy_equity):.2%}"
    )
    print(
        f"Annual volatility: "
        f"{calculate_annual_volatility(strategy_returns):.2%}"
    )
    print(
        f"Sharpe ratio: "
        f"{calculate_sharpe_ratio(strategy_returns):.2f}"
    )
    print()

    print("=== Buy and Hold ===")
    print(f"Final equity: {buy_hold_equity.iloc[-1]:.2f}")
    print(f"CAGR: {calculate_cagr(buy_hold_equity):.2%}")
    print(
        f"Maximum drawdown: "
        f"{calculate_max_drawdown(buy_hold_equity):.2%}"
    )
    print(
        f"Annual volatility: "
        f"{calculate_annual_volatility(buy_hold_returns):.2%}"
    )
    print(
        f"Sharpe ratio: "
        f"{calculate_sharpe_ratio(buy_hold_returns):.2f}"
    )