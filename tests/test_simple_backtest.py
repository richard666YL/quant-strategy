from quant_strategy.backtest.simple_backtest import run_backtest
from quant_strategy.signals.ma_cross_signal import generate_ma_cross_signal
from quant_strategy.utils.data_loader import load_daily_data


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

print(result.tail())
print()

print(f"策略最终净值: {result['strategy_equity'].iloc[-1]:.2f}")
print(f"买入持有最终净值: {result['buy_hold_equity'].iloc[-1]:.2f}")