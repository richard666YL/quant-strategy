from quant_strategy.broker.moomoo_position import (
    get_current_position,
)
from quant_strategy.execution.executor import (
    execute_trade,
)
from quant_strategy.strategies.ma_target_position import (
    calculate_ma_target_position,
)
from quant_strategy.trader.decision import (
    decide_action,
)
from quant_strategy.utils.data_loader import (
    load_daily_data,
)


SYMBOL = "US.QQQ"
DATA_TICKER = "QQQ"
SHORT_WINDOW = 20
LONG_WINDOW = 50
ORDER_QUANTITY = 1


def main() -> None:
    # 1. 读取 QQQ 历史日线数据
    data = load_daily_data(DATA_TICKER)

    # 2. 根据 MA20 / MA50 计算目标仓位
    target_position = calculate_ma_target_position(
        prices=data["Adj Close"],
        short_window=SHORT_WINDOW,
        long_window=LONG_WINDOW,
    )

    # 3. 从 Moomoo 模拟账户读取当前 QQQ 仓位
    current_position = get_current_position(SYMBOL)

    # 4. 比较目标仓位和当前仓位，生成 BUY / SELL / HOLD
    action = decide_action(
        target_position=target_position,
        current_position=current_position,
    )

    # 5. 打印策略运行摘要
    print("=" * 40)
    print("MA20 / MA50 Trading Summary")
    print("=" * 40)
    print(f"Symbol          : {SYMBOL}")
    print(f"Short MA        : {SHORT_WINDOW}")
    print(f"Long MA         : {LONG_WINDOW}")
    print(f"Target Position : {target_position}")
    print(f"Current Position: {current_position}")
    print(f"Decision        : {action}")
    print("=" * 40)

    # 6. 调用执行器
    # 目前 executor.py 是 Dry Run 版本，只打印计划，不会下单
    execute_trade(
        action=action,
        symbol=SYMBOL,
        quantity=ORDER_QUANTITY,
    )


if __name__ == "__main__":
    main()