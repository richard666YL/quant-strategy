from quant_strategy.backtest.simple_backtest import run_backtest
from quant_strategy.performance.metrics import (
    calculate_annual_volatility,
    calculate_cagr,
    calculate_max_drawdown,
    calculate_sharpe_ratio,
)
from quant_strategy.signals.ma_cross_signal import generate_ma_cross_signal
from quant_strategy.utils.data_loader import load_daily_data
from quant_strategy.performance.report import print_performance_report


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

strategy_cagr = calculate_cagr(result["strategy_equity"])
buy_hold_cagr = calculate_cagr(result["buy_hold_equity"])

strategy_drawdown = calculate_max_drawdown(result["strategy_equity"])
buy_hold_drawdown = calculate_max_drawdown(result["buy_hold_equity"])

strategy_volatility = calculate_annual_volatility(
    result["strategy_return"]
)
buy_hold_volatility = calculate_annual_volatility(
    result["asset_return"]
)

strategy_sharpe = calculate_sharpe_ratio(
    result["strategy_return"]
)
buy_hold_sharpe = calculate_sharpe_ratio(
    result["asset_return"]
)

print_performance_report(
    result=result,
    strategy_name="MA20 / MA50",
)