from quant_strategy.signals.ma_cross_signal import generate_ma_cross_signal
from quant_strategy.utils.data_loader import load_daily_data


data = load_daily_data("QQQ")

signals = generate_ma_cross_signal(
    price=data["Adj Close"],
    short_window=20,
    long_window=50,
)

print(signals.tail(20))
print()

print("最近买入信号：")
print(signals[signals["signal"] == 1].tail())
print()

print("最近卖出信号：")
print(signals[signals["signal"] == -1].tail())