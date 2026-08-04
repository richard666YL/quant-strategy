from pathlib import Path

import matplotlib.pyplot as plt

from quant_strategy.backtest.simple_backtest import run_backtest
from quant_strategy.signals.ma_cross_signal import generate_ma_cross_signal
from quant_strategy.utils.data_loader import load_daily_data


PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = PROJECT_ROOT / "reports"


def main() -> None:
    data = load_daily_data("QQQ")

    signals = generate_ma_cross_signal(
        price=data["Adj Close"],
        short_window=20,
        long_window=50,
    )

    result = run_backtest(
        price=data["Adj Close"],
        position=signals["position"],
        trading_cost=0.001,
    )

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    # 资金曲线
    plt.figure(figsize=(12, 6))

    plt.plot(
        result.index,
        result["strategy_equity"],
        label="MA20 / MA50",
    )

    plt.plot(
        result.index,
        result["buy_hold_equity"],
        label="Buy and Hold",
    )

    plt.title("QQQ Strategy Equity vs Buy and Hold")
    plt.xlabel("Date")
    plt.ylabel("Equity")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    equity_file = REPORTS_DIR / "qqq_equity_curve.png"
    plt.savefig(equity_file, dpi=150)
    plt.show()
    plt.close()

    # 回撤曲线
    strategy_drawdown = (
        result["strategy_equity"]
        / result["strategy_equity"].cummax()
        - 1
    )

    buy_hold_drawdown = (
        result["buy_hold_equity"]
        / result["buy_hold_equity"].cummax()
        - 1
    )

    plt.figure(figsize=(12, 6))

    plt.plot(
        result.index,
        strategy_drawdown,
        label="MA20 / MA50",
    )

    plt.plot(
        result.index,
        buy_hold_drawdown,
        label="Buy and Hold",
    )

    plt.title("QQQ Drawdown Comparison")
    plt.xlabel("Date")
    plt.ylabel("Drawdown")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    drawdown_file = REPORTS_DIR / "qqq_drawdown_curve.png"
    plt.savefig(drawdown_file, dpi=150)
    plt.show()
    plt.close()

    print(f"资金曲线已保存：{equity_file}")
    print(f"回撤曲线已保存：{drawdown_file}")


if __name__ == "__main__":
    main()