from quant_strategy.broker.moomoo_position import (
    get_current_position,
)


current_position = get_current_position("US.QQQ")

print(f"QQQ 当前仓位：{current_position}")

if current_position == 1:
    print("账户当前持有 QQQ")
else:
    print("账户当前没有持有 QQQ")