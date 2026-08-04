from quant_strategy.strategies.ma_target_position import (
    calculate_ma_target_position,
)
from quant_strategy.utils.data_loader import load_daily_data


data = load_daily_data("QQQ")

target_position = calculate_ma_target_position(
    prices=data["Adj Close"],
    short_window=20,
    long_window=50,
)

print(f"目标仓位：{target_position}")

if target_position == 1:
    print("策略判断：应该持有 QQQ")
else:
    print("策略判断：应该空仓")